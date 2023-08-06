# coding: utf-8

"""
    Kloudio APIs

"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "Kloudio"
VERSION = "1.0.0"
AUTHOR = "Kloudio"
AUTHOR_EMAIL = "developer@kloud.io"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]

setup(
    name=NAME,
    version=VERSION,
    description="Kloudio APIs",
    author=AUTHOR,
    author_email= AUTHOR_EMAIL,
    url="https://github.com/Kloudio/sdk-python",
    keywords=["SDK", "API", "Kloudio APIs"],
    install_requires=REQUIRES,
    packages=find_packages(exclude=["test", "tests"]),
    include_package_data=True,
    long_description_content_type="text/markdown",
    long_description="""\
    # Kloudio Python Library

- API version: BETA
- Package version: 1.0.0

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

```sh
pip install kloudio
```
(you may need to run `pip` with root permission: `sudo pip install kloudio`)

Then import the package:
```python
import kloudio
```

## Using Kloudio API

Documentation for the Python library can be found at https://github.com/Kloudio/sdk-python



    """
)
