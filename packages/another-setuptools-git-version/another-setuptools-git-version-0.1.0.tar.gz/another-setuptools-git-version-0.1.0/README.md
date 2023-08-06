# another-setuptools-git-version

[![PackageVersion][pypi-version]][pypi-home]
[![PythonVersion][python-version]][python-home]
[![Stable][pypi-status]][pypi-home]
[![Format][pypi-format]][pypi-home]
[![License][pypi-license]](LICENSE)

[pypi-version]: https://badge.fury.io/py/another-setuptools-git-version.svg
[pypi-license]: https://img.shields.io/pypi/l/another-setuptools-git-version.svg
[pypi-status]: https://img.shields.io/pypi/status/another-setuptools-git-version.svg
[pypi-format]: https://img.shields.io/pypi/format/another-setuptools-git-version.svg
[pypi-home]: https://badge.fury.io/py/another-setuptools-git-version
[python-version]: https://img.shields.io/pypi/pyversions/another-setuptools-git-version.svg
[python-home]: https://python.org

Automatically set package version from Git. This is a re-release of
[bad-setuptools-git-version][] with fixes and improvements, which is itself a re-release of [setuptools-git-version][]

[setuptools-git-version]: https://github.com/pyfidelity/setuptools-git-version


## Introduction

Instead of hard-coding the package version in ``setup.py`` like:

```python
setup(
    name='foobar',
    version='1.0.0',
    ...
)
```

this package allows to extract it from tags in the underlying Git repository:

```python
setup(
    name='foobar',
    version_config={
        "version_format": "{tag}.{cc}",
        "starting_version": "0.1.0"
    },
    setup_requires=['another-setuptools-git-version'],
    ...
)
```

The tool uses the semantically-latest tag as the base version. If there are no annotated tags, the version specified by `starting_version` will be used. If `HEAD` is at the tag, the version will be the tag itself. If there are commits ahead of the tag, the commit count will be included.
