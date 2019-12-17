#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='dropbox-filemanager',
    packages=['src'],
    version='0.0.1',
    description="An application to manage files in dropbox account",
    long_description=open('README.md').read(),
    keywords=['file', 'manager', 'dropbox'],
    author="dslackw",
    author_email="d.zlatanidis@gamil.com",
    url="https://gitlab.com/dslackw/dropbox-filemanager",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
        ]
)
