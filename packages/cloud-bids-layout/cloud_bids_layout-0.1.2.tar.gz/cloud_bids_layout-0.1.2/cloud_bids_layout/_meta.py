import os.path as op
import glob

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Natural Language :: English",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Topic :: Scientific/Engineering",
]

# Description should be a one-liner:
description = "Cloud-BIDS-Layout: Use pybids with Amazon S3"

NAME = "cloud_bids_layout"
MAINTAINER = "Adam Richie-Halford"
MAINTAINER_EMAIL = "richiehalford@gmail.com"
DESCRIPTION = description
URL = "https://github.com/nrdg/cloud_bids_layout"
DOWNLOAD_URL = ""
LICENSE = "MIT"
AUTHOR = "Adam Richie-Halford"
AUTHOR_EMAIL = "richiehalford@gmail.com"
PLATFORMS = "OS Independent"
SCRIPTS = [op.join("bin", op.split(f)[-1]) for f in glob.glob("bin/*")]
PYTHON_REQUIRES = ">=3.6"
