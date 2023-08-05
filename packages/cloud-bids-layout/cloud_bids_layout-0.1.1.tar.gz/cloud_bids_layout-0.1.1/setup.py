#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages
import string
import os.path as op
from setuptools_scm import get_version
import glob

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open("CHANGES.rst") as changes_file:
    CHANGES = changes_file.read()

here = op.abspath(op.dirname(__file__))

# Get metadata from the cloud_bids_layout/_meta.py file:
meta_file = op.join(here, "cloud_bids_layout", "_meta.py")
with open(meta_file) as f:
    exec(f.read())

REQUIRES = []
with open(op.join(here, "requirements.txt")) as f:
    ll = f.readline()[:-1]
    while ll:
        REQUIRES.append(ll)
        ll = f.readline()[:-1]

EXTRAS_REQUIRE = {}
for extra_req_file in glob.glob(op.join(here, "requirements-*.txt")):
    extra_name = extra_req_file.split("-")[1].split(".")[0]
    extra_reqs = []
    with open(extra_req_file) as f:
        ll = f.readline()[:-1]
        while ll:
            extra_reqs.append(ll)
            ll = f.readline()[:-1]
    EXTRAS_REQUIRE[extra_name] = extra_reqs

with open(op.join(here, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()


def local_version(version):
    """
    Patch in a version that can be uploaded to test PyPI
    """
    scm_version = get_version()
    if "dev" in scm_version:
        gh_in_int = []
        for char in version.node:
            if char.isdigit():
                gh_in_int.append(str(char))
            else:
                gh_in_int.append(str(string.ascii_letters.find(char)))
        return "".join(gh_in_int)
    else:
        return ""


opts = dict(
    name=NAME,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    download_url=DOWNLOAD_URL,
    license=LICENSE,
    classifiers=CLASSIFIERS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    platforms=PLATFORMS,
    packages=find_packages(),
    install_requires=REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    scripts=SCRIPTS,
    python_requires=PYTHON_REQUIRES,
    use_scm_version={
        "root": ".",
        "relative_to": __file__,
        "write_to": "cloud_bids_layout/version.py",
        "local_scheme": local_version,
    },
    setup_requires=["setuptools_scm"],
)


if __name__ == "__main__":
    setup(**opts)
