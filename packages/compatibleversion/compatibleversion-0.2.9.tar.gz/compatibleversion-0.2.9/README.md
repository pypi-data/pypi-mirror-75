[![License](https://img.shields.io/github/license/YakDriver/compatibleversion.svg)](./LICENSE)
[![Travis CI Build Status](https://travis-ci.org/YakDriver/compatibleversion.svg)](https://travis-ci.org/YakDriver/compatibleversion)
[![Latest Version](https://img.shields.io/pypi/v/compatibleversion.svg?label=version)](https://pypi.python.org/pypi/compatibleversion)

# compatibleversion

*compatibleversion* takes two parameters, a version and a specifier (i.e., version constraints), and returns a Boolean value indicating compatibility.

**NOTE:** *compatibleversion* wraps [packaging](https://packaging.pypa.io/en/latest/) in order to simplify and test its use. Versions and specifiers provided to *compatibleversion* must conform to [PEP 440](https://www.python.org/dev/peps/pep-0440/) as required by *packaging*.

## install

```console
$ pip install compatibleversion
```

## usage

Use *compatibleversion* in Python code:

```python
from compatibleversion import check_version

check_version('1.3.0', '> 1.2, < 3.3')          # True
check_version('2.1', '~= 2.2')                  # False

check_version('1.1.dev0', '>=1.0')              # True
check_version('1.1.dev0', '>=1.0', False)       # False, not allowing pre/dev-final comparison

check_version('1.1.dev0', '>=1.0.dev0')         # True, dev-dev compare
check_version('1.1.dev0', '>=1.0.dev0', False)  # True, doesn't affect since dev-dev
```

## version parameter

The version parameter must conform to [PEP 440](https://www.python.org/dev/peps/pep-0440/). These are examples of valid version parameters:

```
1.2.0
0.0.0
0.9
0.9.1
0.9.2
0.9.10
0.9.11
1.0
1.0.1
1.1
2.0
2.0.1
1.0a1
1.0a2
1.0b1
1.0rc1
1.0.dev1
1.0.dev2
1.0.dev3
1.0.dev4
1.0b2.post345.dev456
1.0b2.post345
1.0rc1.dev456
```

## specifier parameter

The version specifier parameter must conform to [PEP 440](https://www.python.org/dev/peps/pep-0440/). The specifier consists of one or more version clauses separated by commas.

For example, these are valid version specifiers (the last two are approximately equivalent):

```
==1.0.1
< 1.2, > 1.3
~= 0.9, >= 1.0, != 1.3.4.*, < 2.0
~= 1.4.5.0
== 1.1.post1
~= 2.2
>= 2.2, == 2.*
```

Here are more helpful specifier examples from [PEP 440](https://www.python.org/dev/peps/pep-0440/) and an explanation of their meaning:

* `~=3.1`: version 3.1 or later, but not version 4.0 or later.
* `~=3.1.2`: version 3.1.2 or later, but not version 3.2.0 or later.
* `~=3.1a1`: version 3.1a1 or later, but not version 4.0 or later.
* `== 3.1`: specifically version 3.1 (or 3.1.0), excludes all pre-releases, post releases, developmental releases and any 3.1.x maintenance releases.
* `== 3.1.*`: any version that starts with 3.1. Equivalent to the ~=3.1.0 compatible release clause.
* `~=3.1.0, != 3.1.3`: version 3.1.0 or later, but not version 3.1.3 and not version 3.2.0 or later.
