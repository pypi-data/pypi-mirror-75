.. highlight:: shell

============
Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

Report Bugs
~~~~~~~~~~~

Report bugs at https://github.com/SFDO-Tooling/CumulusCI/issues.

When reporting a bug, please include:

* Your operating system name and version.
* Any details about your local setup that might be helpful in troubleshooting.
* Detailed steps to reproduce the bug.

Fix Bugs
~~~~~~~~

Look through the GitHub issues for bugs. Anything tagged with "bug" and "help wanted" is open to whomever wants to implement it.

Implement Features
~~~~~~~~~~~~~~~~~~

Look through the GitHub issues for features. Anything tagged with "enhancement" and "help wanted" is open to whomever wants to implement it.

Write Documentation
~~~~~~~~~~~~~~~~~~~

CumulusCI could always use more documentation, whether as part of the official CumulusCI docs, in docstrings, or even on the web in blog posts, articles, and such.

Submit Feedback
~~~~~~~~~~~~~~~

The best way to send feedback is to file an issue at https://github.com/SFDO-Tooling/CumulusCI/issues.

If you are proposing a feature:

* Explain in detail how it would work.
* Keep the scope as narrow as possible, to make it easier to implement.
* Remember that this is a volunteer-driven project, and that contributions are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up CumulusCI for local development.

1. Fork the CumulusCI repo on GitHub.
2. Clone your fork to your local workspace.
3. Create a fresh virtual environment using virtualenv and install development requirements::

    $ pip install -r requirements_dev.txt

4. Install ``pre-commit`` hooks for ``black`` and ``flake8``::

    $ pre-commit install --install-hooks

5. After making changes, run the tests and make sure they all pass::

    $ pytest

6. Your new code should also have meaningful tests. One way to double check that
   your tests cover everything is to ensure that your new code has test code coverage:

   $ make coverage

7. Push your changes to GitHub and submit a pull request. The base branch should be a new feature branch that we create to receive the changes (contact us to create the branch). This allows us to test the changes using our build system before merging to master.

Note that we enable typeguard with pytest so if you add type declarations to your 
code, those declarations will be treated as runtime assertions in your python
tests. MyPy validation is also on our roadmap.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

* Documentation is updated to reflect all changes.
* New classes, functions, etc have docstrings.
* New code has comments.
* Code style and file structure is similar to the rest of the project.
* You have run the `black` code formatter.

Releasing CumulusCI
-------------------

It's easy to release a version of CumulusCI to GitHub and PyPI! First, create a new branch for your version::

    $ git checkout -b feature/newversion

Make the necessary changes to prepare the new release:

    1. Update the version in ``cumulusci/version.txt``
    2. Update the release notes in ``HISTORY.rst``

Commit the changes, open a Pull Request on GitHub and request approval from another committer.
Once your PR has been merged, a GitHub action will automatically create the release tag and push the artifacts to PyPI.

After a couple minutes, check for the new release's appearance at https://pypi.org/project/cumulusci/

Next, head to the Release object that was autocreated in the GitHub repository, edit it, paste in the changelog notes and hit publish.

You can then create a pull request to update the `Homebrew Tap`_ by running this locally (note, it's important to do this as soon as possible after the release is published on PyPI, because PyPI is the source CumulusCI checks to see if a new version is available)::

    $ git checkout master
    $ git pull
    $ make release-homebrew

That will create a new pull request in the SFDO-Tooling/homebrew-sfdo repository, which can be merged if its tests pass.

Finally, post the release notes to our usual channels:

- CumulusCI Release Announcements group in the Power of Us Hub https://powerofus.force.com/s/group/0F91E000000DHjTSAW/cumulusci-release-announcements
- CumulusCI group in the Trailblazer community https://success.salesforce.com/_ui/core/chatter/groups/GroupProfilePage?g=0F9300000009M9ZCAU

Configuring Your Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``release-homebrew`` build step depends on the `jq`_ command line utility and is available via Homebrew or your package manager.

.. _pypirc: https://docs.python.org/distutils/packageindex.html#the-pypirc-file
.. _Homebrew Tap: https://github.com/SFDO-Tooling/homebrew-sfdo
.. _jq: https://stedolan.github.io/jq/
