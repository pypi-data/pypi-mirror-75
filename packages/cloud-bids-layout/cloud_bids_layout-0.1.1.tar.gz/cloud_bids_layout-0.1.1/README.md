[![Build Status](https://github.com/nrdg/cloudknot/workflows/build/badge.svg)](https://github.com/nrdg/cloud_bids_layout/actions?query=workflow%3Abuild)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

# Cloud-BIDS-Layout

Cloud-BIDS-Layout is a lightweight wrapper for pybids' BIDS.Layout that can
grab BIDS studies from Amazon S3.

## Motivation

The [Brain Imaging Data Structure (BIDS)](https://bids.neuroimaging.io/)
is an intuitive, accessible, and community-driven data specification for
neuroimaging data. [Pybids](https://bids-standard.github.io/pybids/) is
an exceptionally written Python library that makes it easy for
researchers to query, summarize, and manipulate BIDS-compliant data.
However, it's workhorse `BIDSLayout` class doesn't index remote datasets
stored in the cloud. That's where Cloud-BIDS-Layout comes in.

Cloud-BIDS-Layout allows its user to specify a remote location for
a BIDS-Compliant dataset. Currently only Amazon S3 locations are
supported but support for Google Cloud Storage and others is coming
soon. Cloud-BIDS-Layout creates a lightweight semblance of the remote
dataset, just enough to pass to pybids' `BIDSLayout` for indexing.
The user can then use pybids' familiar `.get()` method to select a
subset of the study that they wish to download to the host. See the
[documentation](https://nrdg.github.io/cloud_bids_layout) for more details.

This is the Cloud-BIDS-Layout development site. You can view the source
code, file new issues, and contribute to Cloud-BIDS-Layouts's development.
If you are just getting started, you should look at the [Cloud-BIDS-Layout
documentation](https://nrdg.github.io/cloud_bids_layout)

## Contributing

We love contributions! Cloud-BIDS-Layout is open source, built on open
source, and we'd love to have you hang out in our community.

We have developed some [guidelines](CONTRIBUTING.md) for contributing to
Cloud-BIDS-Layout.

**Imposter syndrome disclaimer**: We want your help. No, really.

There may be a little voice inside your head that is telling you that
you're not ready to be an open source contributor; that your skills
aren't nearly good enough to contribute. What could you possibly offer a
project like this one?

We assure you - the little voice in your head is wrong. If you can
write code at all, you can contribute code to open source. Contributing
to open source projects is a fantastic way to advance one's coding
skills. Writing perfect code isn't the measure of a good developer (that
would disqualify all of us!); it's trying to create something, making
mistakes, and learning from those mistakes. That's how we all improve,
and we are happy to help others learn.

Being an open source contributor doesn't just mean writing code, either.
You can help out by writing documentation, tests, or even giving
feedback about the project (and yes - that includes giving feedback
about the contribution process). Some of these contributions may be the
most valuable to the project as a whole, because you're coming to the
project with fresh eyes, so you can see the errors and assumptions that
seasoned contributors have glossed over.

## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.

The imposter syndrome disclaimer was originally written by
[Adrienne Lowe](https://github.com/adriennefriend) for a [PyCon
talk](https://www.youtube.com/watch?v=6Uj746j9Heo), and was
adapted based on its use in the README file for the [MetPy
project](https://github.com/Unidata/MetPy).
