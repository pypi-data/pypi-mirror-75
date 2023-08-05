Welcome to Cloud-BIDS-Layout's documentation!
=============================================

Cloud-BIDS-Layout is a lightweight wrapper for pybids' BIDS.Layout that
can grab BIDS studies from Amazon S3.

Motivation
----------

The `Brain Imaging Data Structure (BIDS) <https://bids.neuroimaging.io/>`_
is an intuitive, accessible, and community-driven data specification for
neuroimaging data. `Pybids <https://bids-standard.github.io/pybids/>`_
is an exceptionally written Python library that makes it easy for
researchers to query, summarize, and manipulate BIDS-compliant data.
However, it's workhorse `BIDSLayout` class doesn't index remote datasets
stored in the cloud. That's where Cloud-BIDS-Layout comes in.

Cloud-BIDS-Layout allows its user to specify a remote location for
a BIDS-Compliant dataset. Currently only Amazon S3 locations are
supported but support for Google Cloud Storage and others is coming
soon. Cloud-BIDS-Layout creates a lightweight semblance of the remote
dataset, just enough to pass to pybids' `BIDSLayout` for indexing.
The user can then use pybids' familiar `.get()` method to select a
subset of the study that they wish to download to the host. See
Usage_ for more details.

Installation and usage
----------------------

To install Cloud-BIDS-Layout and see usage details
visit :ref:`installation-label` and Usage_.

Documentation and API
---------------------

Most users will only need to interact with the `CloudBIDSLayout` class. See
Usage_ for more details.

Bugs and issues
---------------

If you are having issues, please let us know by `opening up a new issue
<https://github.com/nrdg/cloud_bids_layout/issues>`_.
You will probably want to tag your issue with the "bug" or "question" label.

Contribute
----------

We invite you to contribute to Cloud-BIDS-Layout. Take a look at the `source code
<https://github.com/nrdg/cloud_bids_layout>`_. Or tackle one of the `open issues
<https://github.com/nrdg/cloud_bids_layout/issues>`_. Issues labeled "help wanted"
or "good first issue" are particularly appropriate for beginners.

License
-------

The project is licensed under the `MIT license
<https://github.com/nrdg/cloud_bids_layout/blob/master/LICENSE>`_.

Acknowledgements
----------------

The development of Cloud-BIDS-Layout is supported through grant
`1RF1MH121868-01 <https://projectreporter.nih.gov/project_info_details.cfm?aid=9886761&icde=46874320&ddparam=&ddvalue=&ddsub=&cr=2&csb=default&cs=ASC&pball=>`_
from the `National Institutes for Mental Health <https://www.nimh.nih.gov/index.shtml>`_/`The BRAIN
Initiative <https://braininitiative.nih.gov/>`_.

We are also grateful for support from the `Gordon and Betty Moore
Foundation <https://www.moore.org/>`_ and the `Alfred P. Sloan Foundation <https://sloan.org.>`_ to the `University of
Washington eScience Institute <http://escience.washington.edu/>`_ Data Science Environment, as well as
support from the `Washington Research Foundation <http://www.wrfseattle.org/>`_ to eScience and to the
`University of Washington Institute for Neuroengineering <http://uwin.washington.edu/>`_.

.. toctree::
   :hidden:

   installation <installation>
   usage <usage.ipynb>
   faq <faq>
   contributing <https://github.com/nrdg/cloud_bids_layout/blob/master/CONTRIBUTING.md>
   code <https://github.com/nrdg/cloud_bids_layout>
   bugs <https://github.com/nrdg/cloud_bids_layout/issues>
   history <history>

.. _Usage: usage.ipynb
