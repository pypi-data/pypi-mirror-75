"""Main module for Cloud-BIDS-Layout."""

import bids
import boto3
import os.path as op
import re
import s3fs
import tempfile

from botocore import UNSIGNED
from botocore.client import Config
from pathlib import Path

__all__ = ["CloudBIDSLayout"]


def _get_s3_client(anon=True):
    """Return a boto3 s3 client

    Global boto clients are not thread safe so we use this function
    to return independent session clients for different threads.

    Parameters
    ----------
    anon : bool, default=True
        Whether to use anonymous connection (public buckets only).
        If False, uses the key/secret given, or boto’s credential
        resolver (client_kwargs, environment, variables, config files,
        EC2 IAM server, in that order)

    Returns
    -------
    s3_client : boto3.client('s3')
    """
    session = boto3.session.Session()
    if anon:
        s3_client = session.client("s3", config=Config(signature_version=UNSIGNED))
    else:
        s3_client = session.client("s3")

    return s3_client


def _get_matching_s3_keys(bucket, prefix="", suffix="", anon=True):
    """Generate all the matching keys in an S3 bucket.

    Parameters
    ----------
    bucket : str
        Name of the S3 bucket

    prefix : str, optional
        Only fetch keys that start with this prefix

    suffix : str, optional
        Only fetch keys that end with this suffix

    anon : bool, default=True
        Whether to use anonymous connection (public buckets only).
        If False, uses the key/secret given, or boto’s credential
        resolver (client_kwargs, environment, variables, config files,
        EC2 IAM server, in that order)

    Yields
    ------
    key : list
        S3 keys that match the prefix and suffix
    """
    s3 = _get_s3_client(anon=anon)
    kwargs = {"Bucket": bucket, "MaxKeys": 1000}

    # If the prefix is a single string (not a tuple of strings), we can
    # do the filtering directly in the S3 API.
    if isinstance(prefix, str) and prefix:
        kwargs["Prefix"] = prefix

    while True:
        # The S3 API response is a large blob of metadata.
        # 'Contents' contains information about the listed objects.
        resp = s3.list_objects_v2(**kwargs)

        try:
            contents = resp["Contents"]
        except KeyError:
            return

        for obj in contents:
            key = obj["Key"]
            if key.startswith(prefix) and key.endswith(suffix):
                yield key

        # The S3 API is paginated, returning up to 1000 keys at a time.
        # Pass the continuation token into the next response, until we
        # reach the final page (when this field is missing).
        try:
            kwargs["ContinuationToken"] = resp["NextContinuationToken"]
        except KeyError:
            break


def _mimic_s3(remote_location, download_dir=None, anon=True):
    """Mimic a dataset located on Amazon S3

    This function downloads all json files and mimics the rest using
    empty files

    Parameters
    ----------
    remote_location : str
        The Amazon S3 URI

    download_dir : str, optional, default=None
        The local directory to which the study will be downloaded.
        All json files will be downloaded and all remaining files
        will be mimicked with empty files of the same name. If None,
        this function will use tempfile.mkdtemp() to create a
        temporary directory. It is the user's responsibility to
        delete this directory when done.

    anon : bool, default=True
        Whether to use anonymous connection (public buckets only).
        If False, uses the key/secret given, or boto’s credential
        resolver (client_kwargs, environment, variables, config files,
        EC2 IAM server, in that order)

    Returns
    -------
    dict
        with keys "download_dir" for the host download directory
        and "host2cloud_file_map", which is itself a dict, where
        the keys are the host filename and the values are the
        cloud locations (e.g. Amazon S3 URIs)
    """
    fs = s3fs.S3FileSystem(anon=anon)

    uri_entities = _parse_s3_uri(remote_location)
    bucket = uri_entities["bucket"]
    s3_prefix = uri_entities["key"]

    s3_keys = _get_matching_s3_keys(bucket=bucket, prefix=s3_prefix, anon=anon)

    if download_dir is None:
        download_dir = tempfile.mkdtemp()

    host2cloud_file_map = {}

    for s3_key in s3_keys:
        rel_key = s3_key.split(s3_prefix)[-1].lstrip("/")
        fname = op.abspath(op.join(download_dir, rel_key))

        complete_s3_key = "/".join([bucket, s3_key])
        host2cloud_file_map[fname] = complete_s3_key

        if op.splitext(fname)[-1] == ".json":
            Path(op.dirname(fname)).mkdir(parents=True, exist_ok=True)
            fs.get(complete_s3_key, fname)
        else:
            Path(op.dirname(fname)).mkdir(parents=True, exist_ok=True)
            Path(fname).touch()

    return {"download_dir": download_dir, "host2cloud_file_map": host2cloud_file_map}


def _parse_s3_uri(s3_uri):
    """Parse an Amazon S3 URI into bucket and key entities

    Parameters
    ----------
    s3_uri : str
        The Amazon S3 URI

    Returns
    -------
    dict
        dict with keys "bucket" and "key"
    """
    # Parse s3_uri into bucket and key
    pattern = r"(s3:\/\/)?(?P<bucket>[^\/]*)\/(?P<key>.*)"
    m = re.match(pattern, s3_uri)
    if m is None:
        raise ValueError(
            f"s3_uri is not a valid URI. It should match the regex "
            f"pattern {pattern}. You provided {s3_uri}."
        )
    else:
        return m.groupdict()


class CloudBIDSLayout(bids.BIDSLayout):
    """A wrapper for bids.BIDSLayout that can access BIDS studies on Amazon S3

    This object uses empty files to mimic the file structure of a BIDS
    study on Amazon S3, downloading only the json files required by
    pybids to parse file entities.

    The remaining parameters from bids.BIDSLayout are listed below to make
    this docstring more useful

    remote_location : str
        Location (URI) of study on Amazon S3
    download_dir : str, optional, default=None
        The local directory to which the study will be downloaded.
        All json files will be downloaded and all remaining files
        will be mimicked with empty files of the same name. If None,
        CloudBIDSLayout will use tempfile.mkdtemp() to create a
        temporary directory. It is the user's responsibility to
        delete this directory when done.
    anon : bool, default=True
        Whether to use anonymous connection (public buckets only).
        If False, uses the key/secret given, or boto’s credential
        resolver (client_kwargs, environment, variables, config
        files, EC2 IAM server, in that order)
    validate : bool, optional
        If True, all files are checked for BIDS compliance
        when first indexed, and non-compliant files are ignored. This
        provides a convenient way to restrict file indexing to only those
        files defined in the "core" BIDS spec, as setting validate=True
        will lead files in supplementary folders like derivatives/, code/,
        etc. to be ignored.
    absolute_paths : bool, optional
        If True, queries always return absolute paths.
        If False, queries return relative paths (for files and
        directories).
    derivatives : bool or str or list, optional
        Specifies whether and/or which
        derivatives to to index. If True, all pipelines found in the
        derivatives/ subdirectory will be indexed. If a str or list, gives
        the paths to one or more derivatives directories to index. If False
        or None, the derivatives/ directory is ignored during indexing, and
        derivatives will have to be added manually via add_derivatives().
        Note: derivatives datasets MUST contain a dataset_description.json
        file in order to be indexed.
    config : str or list or None, optional
        Optional name(s) of configuration file(s) to use.
        By default (None), uses 'bids'.
    sources : :obj:`bids.layout.BIDSLayout` or list or None, optional
        Optional BIDSLayout(s) from which the current BIDSLayout is derived.
    ignore : str or SRE_Pattern or list
        Path(s) to exclude from indexing. Each
        path is either a string or a SRE_Pattern object (i.e., compiled
        regular expression). If a string is passed, it must be either an
        absolute path, or be relative to the BIDS project root. If an
        SRE_Pattern is passed, the contained regular expression will be
        matched against the full (absolute) path of all files and
        directories. By default, indexing ignores all files in 'code/',
        'stimuli/', 'sourcedata/', 'models/', and any hidden files/dirs
        beginning with '.' at root level.
    force_index : str or SRE_Pattern or list
        Path(s) to forcibly index in the
        BIDSLayout, even if they would otherwise fail validation. See the
        documentation for the ignore argument for input format details.
        Note that paths in force_index takes precedence over those in
        ignore (i.e., if a file matches both ignore and force_index, it
        *will* be indexed).
        Note: NEVER include 'derivatives' here; use the derivatives argument
        (or :obj:`bids.layout.BIDSLayout.add_derivatives`) for that.
    config_filename : str
        Optional name of filename within directories
        that contains configuration information.
    regex_search : bool
        Whether to require exact matching (True) or regex
        search (False, default) when comparing the query string to each
        entity in .get() calls. This sets a default for the instance, but
        can be overridden in individual .get() requests.
    database_path : str
        Optional path to directory containing SQLite database file index
        for this BIDS dataset. If a value is passed and the folder
        already exists, indexing is skipped. By default (i.e., if None),
        an in-memory SQLite database is used, and the index will not
        persist unless .save() is explicitly called.
    reset_database : bool
        If True, any existing directory specified in the
        database_path argument is deleted, and the BIDS dataset provided
        in the root argument is reindexed. If False, indexing will be
        skipped and the existing database file will be used. Ignored if
        database_path is not provided.
    index_metadata : bool
        If True, all metadata files are indexed at
        initialization. If False, metadata will not be available (but
        indexing will be faster).
    """

    def __init__(
        self,
        remote_location,
        download_dir=None,
        anon=True,
        validate=True,
        absolute_paths=True,
        derivatives=False,
        config=None,
        sources=None,
        ignore=None,
        force_index=None,
        config_filename="layout_config.json",
        regex_search=False,
        database_path=None,
        database_file=None,
        reset_database=False,
        index_metadata=True,
    ):
        mimic = _mimic_s3(
            remote_location=remote_location, download_dir=download_dir, anon=anon
        )
        bids_dir = mimic["download_dir"]

        self._remote_uri = remote_location
        self._download_dir = bids_dir
        self._host2cloud_file_map = mimic["host2cloud_file_map"]
        self._anon = anon
        self._downloaded_from_cloud = []

        super().__init__(
            root=bids_dir,
            validate=validate,
            absolute_paths=absolute_paths,
            derivatives=derivatives,
            config=config,
            sources=sources,
            ignore=ignore,
            force_index=force_index,
            config_filename=config_filename,
            regex_search=regex_search,
            database_path=database_path,
            database_file=database_file,
            reset_database=reset_database,
            index_metadata=index_metadata,
        )

    def download_files(
        self,
        return_type="object",
        target=None,
        scope="all",
        regex_search=False,
        absolute_paths=None,
        invalid_filters="error",
        **filters,
    ):
        """Wrapper for bids.BIDSLayout().get()

        Retrieves files and/or metadata from the current Layout
        and downloads the resulting files. The remaining
        parameters for bids.BIDSLayout().get are listed below to
        make this docstring more useful.

        Parameters
        ----------
        return_type : str, optional
            Type of result to return. Valid values:
            'object' (default): return a list of matching BIDSFile objects.
            'file' or 'filename': return a list of matching filenames.
            'dir': return a list of directories.
            'id': return a list of unique IDs. Must be used together
                  with a valid target.
        target : str, optional
            Optional name of the target entity to get results for
            (only used if return_type is 'dir' or 'id').
        scope : str or list, optional
            Scope of the search space. If passed, only
            nodes/directories that match the specified scope will be
            searched. Possible values include:
            'all' (default): search all available directories.
            'derivatives': search all derivatives directories.
            'raw': search only BIDS-Raw directories.
            'self': search only the directly called BIDSLayout.
            <PipelineName>: the name of a BIDS-Derivatives pipeline.
        regex_search : bool or None, optional
            Whether to require exact matching
            (False) or regex search (True) when comparing the query string
            to each entity.
        absolute_paths : bool, optional
            Optionally override the instance-wide option
            to report either absolute or relative (to the top of the
            dataset) paths. If None, will fall back on the value specified
            at BIDSLayout initialization.
        invalid_filters (str): Controls behavior when named filters are
            encountered that don't exist in the database (e.g., in the case of
            a typo like subbject='0.1'). Valid values:
                'error' (default): Raise an explicit error.
                'drop': Silently drop invalid filters (equivalent to not having
                    passed them as arguments in the first place).
                'allow': Include the invalid filters in the query, resulting
                    in no results being returned.
        filters : dict
            Any optional key/values to filter the entities on.
            Keys are entity names, values are regexes to filter on. For
            example, passing filters={'subject': 'sub-[12]'} would return
            only files that match the first two subjects. In addition to
            ordinary data types, the following enums are defined (in the
            Query class):
                * Query.NONE: The named entity must not be defined.
                * Query.ANY: the named entity must be defined, but can have any
                    value.
        Returns
        -------
        list of :obj:`bids.layout.BIDSFile` or str
            A list of BIDSFiles (default) or strings (see return_type).
        """
        valid_return_types = ["object", "file", "filename"]
        if return_type not in valid_return_types:
            return ValueError(f"return_type must be one of {valid_return_types}.")

        results = super().get(
            return_type=return_type,
            target=target,
            scope=scope,
            regex_search=regex_search,
            absolute_paths=absolute_paths,
            invalid_filters=invalid_filters,
            **filters,
        )

        if return_type.startswith("file"):
            fnames = [f for f in results]
        else:
            fnames = [f.path for f in results]

        fs = s3fs.S3FileSystem(anon=self._anon)
        for fname in fnames:
            s3_key = self._host2cloud_file_map[op.abspath(fname)]
            fs.get(s3_key, fname)

        return results
