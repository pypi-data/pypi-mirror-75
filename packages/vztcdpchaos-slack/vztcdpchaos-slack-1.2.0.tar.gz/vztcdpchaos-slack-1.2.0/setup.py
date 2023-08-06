#!/usr/bin/env python
"""chaosutil extension builder and installer"""

import sys
import io

import setuptools

name = 'vztcdpchaos-slack'
desc = 'Slack extension for cdp chaos exps'

classifiers = [

    'Intended Audience :: Developers',
    'License :: Freely Distributable',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: Apache Software License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: Implementation',
    'Programming Language :: Python :: Implementation :: CPython'
]
author = "vzt-cdp"
license = 'Apache License Version 2.0'
packages = [
    'cdpchaosslack'
]

setup_params = dict(
    name=name,
    version='1.2.0',
    description=desc,
    classifiers=classifiers,
    author=author,
    license=license,
    packages=packages,
    include_package_data=True,
    install_requires=['slackclient>=2.2.0',
                      'chaostoolkit-lib>=1.7.0',
                      'logzero',
                      'cdpchaostoolkit'
                      ],
    python_requires='>=3.5.*'
)


def main():
    """Package installation entry point."""
    setuptools.setup(**setup_params)


if __name__ == '__main__':
    main()
