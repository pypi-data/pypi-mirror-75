# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.


## Types of Contributions

You can contribute in many ways:

### Report Bugs

Report bugs at <https://github.com/nrdg/cloud_bids_layout/issues>.

If you are reporting a bug, please include:

- Your operating system name and version.
- Any details about your local setup that might be helpful in troubleshooting.
- Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help
wanted" is open to whoever wants to implement it. The maintainers will also
try to "good first issue" tag to label issues that we think would be especially
appropriate for those new to open-source software contribution.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "enhancement"
and "help wanted" is open to whoever wants to implement it.

### Write Documentation

Cloud-BIDS-Layout could always use more documentation, whether as part of the
official Cloud-BIDS-Layout docs, in docstrings, or even on the web in blog posts,
articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at
<https://github.com/nrdg/cloud_bids_layout/issues>.

If you are proposing a feature:

- Explain in detail how it would work.

- Keep the scope as narrow as possible, to make it easier to implement.

- Remember that this is a volunteer-driven project, and that contributions
  are welcome :)

## Get Started!

Ready to contribute? Here's how to set up `cloud_bids_layout` for local development.

1. Fork the `cloud_bids_layout` repo on GitHub.
1. Clone your fork locally:

   ```bash
   $ git clone git@github.com:your_name_here/cloud_bids_layout.git
   ```

1. Activate the pre-commit formatting hook:
   ```bash
   pre-commit install
   ```

1. It's a good idea to use a virtualenv or conda environment to isolate your
   Cloud-BIDS-Layout development environment from your systems Python
   installation.
   Assuming you have virtualenvwrapper installed, this is how you
   set up your environment for local development:
   ```bash
   $ mkvirtualenv
   ```
   If you are using conda, use
   ```bash
   $ conda create --name cloud_bids_layout python=3.7 --no-default-packages
   ```

1. Install your local copy:
   ```bash
   $ cd cloud_bids_layout/
   $ pip install -e .[dev]
   ```

1. Create a branch for local development::
   ```bash
   $ git checkout -b name-of-your-bugfix-or-feature
   ```
   Now you can make your changes locally.

1. When you're done making changes, check that your changes pass the linting
   and unit tests:
   ```bash
   $ make lint
   $ make test
   ```

1. Commit your changes and push your branch to GitHub::
   ```bash
   $ git add .
   $ git commit -m "Your detailed description of your changes."
   $ git push origin name-of-your-bugfix-or-feature
   ```

1. Submit a pull request (PR) through the GitHub website. The output of the
   last `git push` command will supply a link that you can use to open the PR.

### Pull Request Guidelines

Before you submit a pull request, check that it meets these guidelines:

1. The pull request should include tests.
1. If the pull request adds functionality, the docs should be updated. Put
   your new functionality into a function with a docstring, and add the
   feature to the list in README.md.
1. The pull request should work for Python 3.5, 3.6, 3.7 and 3.8, and for PyPy. Check
   https://travis-ci.com/nrdg/cloud_bids_layout/pull_requests
   and make sure that the tests pass for all supported Python versions.

## Maintainers

A reminder for the maintainers on how to deploy.
Cloud-BIDS-Layout pushes a development version to
[Test-PyPI](https://test.pypi.org/) on every pull request merged into
the master branch. To release a new version, use the
`publish_release.sh` script from the root directory, i.e.:
```bash
.maintenance/publish_release.sh <version_number>
```
For releases, use the following format for <version_number>:
"v<major>.<minor>.<micro>".
When executed, this will ask you if you want to customize the
`CHANGES.rst` document or the release notes. After that,
GitHub actions will take care of publishing the new release on PyPI and
creating a release on GitHub.

