# Wardoff

[![Build Status](https://travis-ci.org/4383/wardoff.svg?branch=master)](https://travis-ci.org/4383/wardoff)
![PyPI](https://img.shields.io/pypi/v/wardoff.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/wardoff.svg)
![PyPI - Status](https://img.shields.io/pypi/status/wardoff.svg)
[![Downloads](https://img.shields.io/pypi/dm/wardoff.svg)](https://pypi.python.org/pypi/wardoff/)

Wardoff (pronounced `ward off`) aim to help you to maintain your code base
clean and up-to-date by reducing the pain of collect informations about all
your underlaying libraries in your stack in a proactively.

Wardoff looking for deprecated stuffs in project requirements and underlying
libraries to help you to keep your code up-to-date.

The main goal of wardoff is to analyze all requirements of a given project
to extract deprecated things from their codes.

For each analyze a dedicated python virtual environment is built and project's
requirements are installed within. Then installed source code files of
project's requirement are analyzed one by one.

Code analyze of the requirements is based on
[AST](https://docs.python.org/3/library/ast.html) and
[python tokens](https://docs.python.org/3/library/tokenize.html). Each
source code file of each underlaying library is analyzed in this way.

You can pass a list of constraints to apply to your analyze to be sure
to match the right versions of your underlaying libraries.

Traditionally projects maintainers are informed that functions will become
deprecated or removed by reading documentation or by
observing deprecation warning at the runtime in logs. When your stack
grow and the number of requirements in your stack increase it could be
painful to stay up-to-date, wardoff aim to collect for you all these infos
by only using 1 command without needing any runtime environment setup.



## Install

Still in development and really unstable, however you can install unstable
development versions by using:

```shell
$ python3 -m pip install --user wardoff
```

## Requirements

- python3.8+
- git

## Usages

### From a named package

Found deprecated things from a named package (directly from pypi):

```sh
$ wardoff niet # will list all deprecations founds in niet is requirements
$ wardoff oslo.messaging # will list all deprecations founds in oslo.messaging is requirements
$ wardoff oslo.messaging==12.2.2 # will list all deprecations founds in oslo.messaging 12.2.2 is requirements
$ wardoff oslo.messaging==1.3.0 # will list all deprecations founds in oslo.messaging 1.3.0 is requirements
```

### From the current directory

(Coming soon - not yet implemented)
Retrieve deprecated things from the current working directory.
Retrieve requirements from:
- `requirements.txt`
- `test-requirements.txt`
- `*-requirements.txt`

Example:

```sh
$ wardoff # will list all deprecations founds in requirements founds in current directory
```

### From a distant repository

(Coming soon - not yet implemented)
Retrieve deprecated things from a distgit repo.

Example:

```sh
$ wardoff https://opendev.org/openstack/nova/ # from opendev.org
$ wardoff https://github.com/openstack/nova # from github.com
$ wardoff git@github.com:openstack/nova # by using git format
```

### From a local repository

(Coming soon - not yet implemented)
Retrieve deprecated things from a distgit repo.

Example:

```sh
$ wardoff ~/dev/nova # from a local clone of openstack/nova
```

## Side features

### tokenizer

Wardoff provide a CLI tokenizer which can be used against code passed through
the CLI or by passing a file path and a specific line to read.

Example with raw code passed through the CLI:

```sh
$ wardoff-tokenizer "def person(name, age):"
TokenInfo(type=62 (ENCODING), string='utf-8', start=(0, 0), end=(0, 0), line='')
TokenInfo(type=1 (NAME), string='def', start=(1, 0), end=(1, 3), line='def person(name, age):')
TokenInfo(type=1 (NAME), string='person', start=(1, 4), end=(1, 10), line='def person(name, age):')
TokenInfo(type=54 (OP), string='(', start=(1, 10), end=(1, 11), line='def person(name, age):')
TokenInfo(type=1 (NAME), string='name', start=(1, 11), end=(1, 15), line='def person(name, age):')
TokenInfo(type=54 (OP), string=',', start=(1, 15), end=(1, 16), line='def person(name, age):')
TokenInfo(type=1 (NAME), string='age', start=(1, 17), end=(1, 20), line='def person(name, age):')
TokenInfo(type=54 (OP), string=')', start=(1, 20), end=(1, 21), line='def person(name, age):')
TokenInfo(type=54 (OP), string=':', start=(1, 21), end=(1, 22), line='def person(name, age):')
TokenInfo(type=4 (NEWLINE), string='', start=(1, 22), end=(1, 23), line='')
TokenInfo(type=0 (ENDMARKER), string='', start=(2, 0), end=(2, 0), line='')
```

Another example by passing a file line to tokenize:

```sh
wardoff-tokenizer ~/dev/wardoff/wardoff/tokenizer.py+12
```

It will tokenize the line number 12 of the file
`~/dev/wardoff/wardoff/tokenizer.py`

For further options with this command:

```sh
$ wardoff-tokenizer -h
```

### freeze

Wardoff allow you to freeze installed requirements. It will provide a similar
output than `pip freeze` but it will only print requirements related the given
package.

Example:

```
$ wardoff-freeze oslo.messaging==1.3.0
amqp==2.6.0
Babel==2.8.0
certifi==2020.6.20
chardet==3.0.4
debtcollector==2.2.0
dnspython==2.0.0
eventlet==0.25.2
greenlet==0.4.16
idna==2.10
iso8601==0.1.12
kombu==4.6.11
monotonic==1.5
netaddr==0.8.0
oslo.config==8.3.1
oslo.i18n==5.0.0
pbr==5.4.5
pytz==2020.1
PyYAML==5.3.1
requests==2.24.0
rfc3986==1.4.0
six==1.15.0
stevedore==3.2.0
urllib3==1.25.10
vine==1.3.0
wrapt==1.12.1
```

## The future of wardoff

We plan to introduce more features like issues and pull requests or
patches harvesting.
