#!/usr/bin/env python
"""cdpchaostoolkit builder and installer"""

import sys
import io
from os.path import abspath, dirname, join, normpath

import setuptools



name = 'cdpchaostoolkit'
desc = 'CDP Chaos Engineering Toolkit'

classifiers = [


    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: Implementation',
    'Programming Language :: Python :: Implementation :: CPython',

]
author = 'vzt-cdp'
author_email = 'suchetha.panduranga@verizonconnect.com'
license = 'Apache Software License 2.0'
packages = [
    'cdpchaostoolkit'
]

install_require = [
    'click>=7.0',
    'click-plugins>=1.0.4',
    'logzero>=1.5.0',
    'chaostoolkit-lib>=1.6.0',
    'requests>=2.21',
    'python-json-logger>=0.1.11',
    'vztcdpchaos-report',
    'vztcdpchaos-slack'

]

setup_params = dict(
    name='cdpchaostoolkit',
    version='1.4.2',
    description="CDP Chaostoolkit - Modified",


    classifiers=classifiers,
    author=author,
    author_email=author_email,

    license=license,
    packages=packages,
    entry_points={'console_scripts': ['chaos = cdpchaostoolkit.__main__:cli']},
    include_package_data=True,
    install_requires=install_require,


    python_requires='>=3.5.*'
)


def main():
    """Package installation entry point."""
    setuptools.setup(**setup_params)


if __name__ == '__main__':
    main()
