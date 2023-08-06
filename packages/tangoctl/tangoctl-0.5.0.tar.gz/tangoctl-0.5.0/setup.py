#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the tangoctl project
#
# Copyright (c) 2018 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

"""The setup script."""

import sys
from setuptools import setup, find_packages

def get_readme(name='README.md'):
    """Get readme file contents without the badges."""
    with open(name) as f:
        return f.read()

readme = get_readme()

requirements = ['pytango', 'click', 'treelib', 'gevent', 'tabulate']

extras_requirements = {
    'repl' : ['prompt_toolkit>=3.0.3']
}

test_requirements = ['pytest', 'pytest-cov']

setup_requirements = []

needs_pytest = {'pytest', 'test'}.intersection(sys.argv)
if needs_pytest:
    setup_requirements.append('pytest-runner')

setup(
    author="Jose Tiago Macara Coutinho",
    author_email='coutinhotiago@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="tango system cli manager",
    entry_points={
        'console_scripts': [
            'tangoctl = tangoctl.cli:cli',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='tango,tangoctl,pytango',
    name='tangoctl',
    packages=find_packages(include=['tangoctl']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    extras_require=extras_requirements,
    python_requires='>=3.5',
    url='https://gitlab.com/tiagocoutinho/tangoctl',
    version='0.5.0',
    zip_safe=True,
)
