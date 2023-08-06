Contributing
============

Contributions are welcome, and they are greatly appreciated! Every little bit helps, and credit will always be given.

You can contribute in many ways:

Types of Contributions
----------------------

### Report Bugs

Report bugs at https://github.com/czbiohub/cerebra/issues.

If you are reporting a bug, please include:

-   Your operating system name and version.
-   Any details about your local setup that might be helpful in troubleshooting.
-   Detailed steps to reproduce the bug.

### Fix Bugs

Look through the GitHub issues for bugs. Anything tagged with "bug" is open to whoever wants to implement it.

### Implement Features

Look through the GitHub issues for features. Anything tagged with "feature" is open to whoever wants to implement it.

### Write Documentation

cerebra could always use more documentation, whether as
part of the official cerebra docs, in docstrings, or
even on the web in blog posts, articles, and such.

### Submit Feedback

The best way to send feedback is to file an issue at https://github.com/czbiohub/cerebra/issues.

If you are proposing a feature:

-   Explain in detail how it would work.
-   Keep the scope as narrow as possible, to make it easier to implement.
-   Remember that this is a volunteer-driven project, and that contributions are welcome :)

Get Started!
------------

Ready to contribute? Here's how to set up cerebra for
local development.

1.  Fork the cerebra repo on GitHub: https://github.com/czbiohub/cerebra
2.  Clone your fork locally:

        $ git clone https://github.com/your-name/cerebra.git

3.  Install your local copy into a virtualenv. Using the standard library [`venv`](https://docs.python.org/3/library/venv.html) module: 

        $ cd cerebra
        $ python3 -m venv cerebra-dev
        $ source cerebra-dev/bin/activate
        $ pip3 install -e . 

4.  Create a branch for local development:

        $ git checkout -b name-of-your-bugfix-or-feature

    Now you can make your changes locally.

5.  When you're done making changes, check that your changes pass flake8 and the tests:

        $ make test
        $ make coverage
        $ make lint

6.  Commit your changes and push your branch to GitHub:

        $ git add .
        $ git commit -m "Your detailed description of your changes."
        $ git push origin name-of-your-bugfix-or-feature

7.  Submit a pull request through the GitHub website.

Pull Request Guidelines
-----------------------

Before you submit a pull request, check that it meets these guidelines:

1.  The pull request should include tests.
2.  Functionality should be encapsulated within a function(s) that includes a docstring. 
3.  The pull request should work for Python 3.6, 3.7 and potentially 3.8. Check
    https://travis-ci.org/github/czbiohub/cerebra/pull_requests and make sure that the tests pass
    for all supported Python versions.

Tips
----

To run a subset of tests:

    $ pytest test_you_want_to_run.py
