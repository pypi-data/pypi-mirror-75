#!/usr/bin/env python

"""Tests for `cloud_bids_layout` package."""

import bids
import botocore
import filecmp
import os
import os.path as op
import pytest
import s3fs
import shutil
from click.testing import CliRunner
from glob import glob
from moto import mock_s3
from cloud_bids_layout import cloud_bids_layout as cbl
from cloud_bids_layout import cli
from uuid import uuid4

DATA_PATH = op.join(op.abspath(op.dirname(__file__)), "data")
TEST_BUCKET = "test-bucket"
TEST_DATASET = "ds000102-mimic"


@pytest.fixture
def temp_data_dir():
    test_dir = str(uuid4())
    os.mkdir(test_dir)

    yield test_dir

    shutil.rmtree(test_dir)


@mock_s3
def s3_setup():
    """pytest fixture to put test_data directory on mock_s3"""
    fs = s3fs.S3FileSystem()
    client = cbl._get_s3_client()
    client.create_bucket(Bucket=TEST_BUCKET)
    fs.put(
        op.join(DATA_PATH, TEST_DATASET),
        "/".join([TEST_BUCKET, TEST_DATASET]),
        recursive=True,
    )


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert "cloud_bids_layout.cli.main" in result.output
    help_result = runner.invoke(cli.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output


@mock_s3
def test_get_s3_client():
    client_anon = cbl._get_s3_client(anon=True)
    assert isinstance(client_anon, botocore.client.BaseClient)
    assert client_anon.meta.service_model.service_id == "S3"
    assert client_anon.meta.config.signature_version == botocore.UNSIGNED

    client = cbl._get_s3_client(anon=False)
    assert isinstance(client, botocore.client.BaseClient)
    assert client.meta.service_model.service_id == "S3"
    assert isinstance(client.meta.config.signature_version, str)


def test_parse_s3_uri():
    # Test for correct parsing with the "s3://" prefix
    parsed = cbl._parse_s3_uri("s3://bucket/key")
    assert parsed["bucket"] == "bucket"
    assert parsed["key"] == "key"

    # Test without it
    parsed = cbl._parse_s3_uri("bucket/key")
    assert parsed["bucket"] == "bucket"
    assert parsed["key"] == "key"

    # Test for ValueError on incorrect formatting
    with pytest.raises(ValueError):
        cbl._parse_s3_uri("foo")


@mock_s3
def test_get_matching_s3_keys():
    s3_setup()

    fnames = []
    for pattern in ["**", "*/.*", "*/.*/.*", "*/.*/**"]:
        fnames += [
            s for s in glob(op.join(DATA_PATH, pattern), recursive=True) if op.isfile(s)
        ]

    fnames = [s.replace(DATA_PATH + "/", "") for s in fnames]

    matching_keys = list(
        cbl._get_matching_s3_keys(bucket=TEST_BUCKET, prefix=TEST_DATASET)
    )

    assert set(fnames) == set(matching_keys)


@mock_s3
def test_mimic_s3_with_named_dir(temp_data_dir):
    s3_setup()

    test_dir = temp_data_dir

    mimic = cbl._mimic_s3(
        "/".join([TEST_BUCKET, TEST_DATASET]), download_dir=test_dir, anon=False
    )
    download_dir = op.abspath(mimic["download_dir"])

    assert download_dir == op.abspath(test_dir)

    download_files = list(mimic["host2cloud_file_map"].keys())
    ref_dir = op.abspath(op.join(DATA_PATH, TEST_DATASET))

    match, mismatch, errors = filecmp.cmpfiles(
        ref_dir, download_dir, download_files, shallow=False
    )

    assert not mismatch
    assert not errors


@mock_s3
def test_mimic_s3_with_temp_dir():
    s3_setup()

    mimic = cbl._mimic_s3(
        "/".join([TEST_BUCKET, TEST_DATASET]), download_dir=None, anon=False
    )
    download_dir = op.abspath(mimic["download_dir"])
    download_files = list(mimic["host2cloud_file_map"].keys())
    ref_dir = op.abspath(op.join(DATA_PATH, TEST_DATASET))

    match, mismatch, errors = filecmp.cmpfiles(
        ref_dir, download_dir, download_files, shallow=False
    )

    shutil.rmtree(download_dir)

    assert not mismatch
    assert not errors


@mock_s3
def test_CloudBIDSLayout(temp_data_dir):
    s3_setup()

    test_dir = temp_data_dir

    cloud_layout = cbl.CloudBIDSLayout(
        remote_location="/".join([TEST_BUCKET, TEST_DATASET]),
        download_dir=test_dir,
        anon=False,
    )

    orig_layout = bids.BIDSLayout(test_dir)

    assert cloud_layout.get(return_type="files") == orig_layout.get(return_type="files")

    cloud_layout.download_files()

    ref_dir = op.abspath(op.join(DATA_PATH, TEST_DATASET))
    test_files = [
        s for s in glob(op.join(test_dir, "**"), recursive=True) if op.isfile(s)
    ]
    test_files = [s.replace(test_dir + "/", "") for s in test_files]

    match, mismatch, errors = filecmp.cmpfiles(
        ref_dir, test_dir, test_files, shallow=False
    )

    assert not mismatch
    assert not errors
