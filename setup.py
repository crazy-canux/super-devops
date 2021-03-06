#!/usr/bin/env python3

"""
SUMMARY setup.py

Copyright (C) 2017 Canux CHENG.
All rights reserved.

LICENSE GNU General Public License v3.0.

:author: Canux CHENG canuxcheng@gmail.com
:since: Wed 01 Nov 2017 09:13:48 AM EDT

DESCRIPTION:
"""
import os

from setuptools import setup, find_packages
from setuptools.command.install import install

import super_devops

NAME = 'super_devops'
VERSION = super_devops.__version__
URL = 'https://github.com/crazy-canux/super-devops'
DESCRIPTION = 'Tons of devops tools used for testing, monitoring, logging...'
KEYWORDS = 'DevOps Monitoring Testing Logging'


def read(readme):
    """Give reST format README for pypi."""
    extend = os.path.splitext(readme)[1]
    if extend == '.rst':
        import codecs
        return codecs.open(readme, 'r', 'utf-8').read()
    elif extend == '.md':
        import pypandoc
        return pypandoc.convert(readme, 'rst')


class InstInstall(install):
    def run(self):
        print("PreInst for super-devops.")
        install.run(self)
        print("PostInst for super-devops.")


INSTALL_REQUIRES = []

setup(
    name=NAME,
    version=VERSION,
    url=URL,
    description=DESCRIPTION,
    keywords=KEYWORDS,
    author='Canux CHENG',
    author_email='canuxcheng@gmail.com',
    maintainer='Canux CHENG',
    maintainer_email='canuxcheng@gmail.com',
    long_description=read('README.rst'),
    license='GPL',
    platforms='any',
    install_requires=INSTALL_REQUIRES,
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    scripts=[],
    data_files=[],
    cmdclass={
        "install": InstInstall
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries"
    ],
)
