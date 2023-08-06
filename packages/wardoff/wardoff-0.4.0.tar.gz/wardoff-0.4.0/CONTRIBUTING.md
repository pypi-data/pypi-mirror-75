# Contributing to wardoff

First off, thanks for taking the time to contribute!

The following as a set of guidelines for contributing to wardoff.
These are mostly guidelines, not rules. Use your best judgment, and fell
free to propose changes to this document in a pull request.

## Code of Conduct

This project and everyone participating in it is governed
by the [wardoff Code of Conduct](CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code.
Please report unacceptable behavior to [herveberaud.pro@gmail.com](mailto:herveberaud.pro@gmail.com).

## How Can I Contribute?

### Reporting Bugs

This section guides you through submitting a bug report for wardoff.
Following these guidelines helps maintainers and the community
understand your report, reproduce the behavior, and find related reports.

Before creating bug reports, please perform a
[cursory search](https://github.com/4383/wardoff/issues?q=is%3Aissue%20is%3Aopen%20)
to see if the problem has already been reported.
If it has and the issue is still open, add a comment to
the existing issue instead of opening a new one.
When you are creating a bug report, please [include as many details as possbile](#how-do-i-submit-a-good-bug-report).

> **Note:** If you find a **Closed** issue that seems like it is the same thing that you're experiencing, open a new issue and include a link to the original issue in the body of your new one.

#### How Do I Submit A (Good) Bug Report?

Bugs are tracked as [GitHub issues](https://guides.github.com/features/issues/).

Explain the problem and include additional details to help maintainers reproduce the problem:

* **Use a clear and descriptive title** for the issue to identify the problem.
* **Describe the exact steps which reproduce the problem** in as many details as possible. For example, start by explaining how you use the wardoff command line, e.g. which command exactly you used in the terminal. When listing steps, **don't just say what you did, but explain how you did it**.
* **Provide specific examples to demonstrate the steps**. Include links to files or GitHub projects, or copy/pasteable snippets, which you use in those examples. If you're providing snippets in the issue, use [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the behavior you observed after following the steps** and point out what exactly is the problem with that behavior.
* **Explain which behavior you expected to see instead and why.**


Provide more context by answering these questions:

* **Did the problem start happening recently** (e.g. after updating to a new version of wardoff) or was this always a problem?
* If the problem started happening recently, **can you reproduce the problem in an older version of wardoff?** What's the most recent version in which the problem doesn't happen? You can install older versions of wardoff from [the pypi repository](https://pypi.org/project/wardoff/).
* **Can you reliably reproduce the issue?** If not, provide details about how often the problem happens and under which conditions it normally happens.

Include details about your configuration and environment:

* **Which version of wardoff are you using?** You can get the exact version by running `pip freeze | grep "wardoff"` in your terminal.
* **What's the name and version of the OS you're using**?
* **What's the version of python you're using**?

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for wardoff, including completely new features and minor improvements to existing functionality. Following these guidelines helps maintainers and the community understand your suggestion and find related suggestions.

When you are creating an enhancement suggestion, please [include as many details as possible](#how-do-i-submit-a-good-enhancement-suggestion) and including the steps that you imagine you would take if the feature you're requesting existed.

#### How Do I Submit A (Good) Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://guides.github.com/features/issues/).

Provide the following information:

* **Use a clear and descriptive title** for the issue to identify the suggestion.
* **Provide a step-by-step description of the suggested enhancement** in as many details as possible.
* **Provide specific examples to demonstrate the steps**. Include copy/pasteable snippets which you use in those examples, as [Markdown code blocks](https://help.github.com/articles/markdown-basics/#multiple-lines).
* **Describe the current behavior** and **explain which behavior you expected to see instead** and why.
* **Include screenshots and animated GIFs** which help you demonstrate the steps or point out the part of wardoff which the suggestion is related to. You can use [this tool](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and [this tool](https://github.com/colinkeenan/silentcast) or [this tool](https://github.com/GNOME/byzanz) on Linux.
* **Explain why this enhancement would be useful** to most wardoff users.
* **List some other tools or applications where this enhancement exists.**
* **Specify which version of wardoff you're using.** You can get the exact version by running `pip freeze| grep "wardoff"` in your terminal.
* **Specify the name and version of the OS you're using.**
* **Specify the version of python you're using**

## Code Contribution

### Contributing on wardoff

If you're hitting a bug in wardoff or just want to experiment with adding a feature, follow these steps.

#### Prerequisites

- [tox](https://tox.readthedocs.io/en/latest/)
- python 2.7+

#### Cloning

```shell
$ git clone https://github.com/4383/wardoff
```

#### Setup your environment

From there, you can navigate into the directory where you've cloned
the wardoff source code

```shell
$ cd wardoff
```
To reduce the pain to format our code we decided to use
[black](https://github.com/psf/black) and
[isort](https://github.com/timothycrosley/isort) to automatically format our
code base.

These 2 utilities are configured to be used through
[pre-commit](https://pre-commit.com/).

To setup our development environment you just have to run the
following commands:

```shell
$ pip install pre-commit
$ pre-commit install
```

Then at each commit your code will be automatically formated to
pass our linters checks.

You can run our hooks manually by using:
```shell
$ pre-commit run --all-files
```

It will execute the same checks and commands than these who will be used
during commit hooks.

Also if you don't want to use pre-commit we allow to you the possibility
to format your code by using tox:

```shel
$ tox -e format
```

`tox` allow you to use wardoff directly in a dedicated virtual environment
already configured (requirements, etc):

```shell
$ tox -e venv -- wardoff -h
...
venv run-test: commands[0] | wardoff -h
...
___________________ summary ______________
  venv: commands succeeded
  congratulations :)
```

#### Make your changes

First create your working branch:
```shell
$ git checkout -b somefeature origin/master
```

> Be sure to create your working branch from `master` and be sure your master are up-to-date

Make our changes:
```shell
$ vim <file-to-edit>
$ git commit -am 'I did some changes'
```

If you configured pre-commit as described previously then your code will be
automatically formated.

#### Ensure everything work fine

Every following checks are automaticaly executed on pull requests so you need to
be sure that all of these checks run successfully before submit your pull request
on github.


Code formating and PEP8 validation:
```shell
$ tox -e pep8
```

Run all unit tests and checks:
```shell
$ tox
```

> Note: If you have just a specific version of python installed on your system, you can test like this:
```shell
$ tox -e py38 # test with python 3.8
```

### Pull Requests

If everything work fine you can create your pull request.

Before ensure you have [squash your commits](http://gitready.com/advanced/2009/02/10/squashing-commits-with-rebase.html).

> Be sure to submit your pull request on the upstream `master` branch!

You can submit your pull request manually directly from github:
* Include examples, outputs, etc... whenever possible.
* Include screenshots and animated GIFs in your pull request whenever possible.

Or by example by using some tools like
[git-pull-request](https://github.com/jd/git-pull-request):

```shell
$ pip install -U git-pull-request # if not installed
$ git pull-request
Forked repository: https://github.com/4383/niet
Force-pushing branch `somefeature' to remote `github'
Counting objects: 5, done.
Delta compression using up to 4 threads.
Compressing objects: 100% (4/4), done.
Writing objects: 100% (5/5), 562 bytes | 0 bytes/s, done.
Total 5 (delta 3), reused 0 (delta 0)
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
To https://github.com/4383/niet.git
 + 73a733f7...1be2bf29 somefeature -> somefeature (forced update)
 Pull-request created: https://github.com/4383/niet/pull/33
```
