#!/usr/bin/env python
# -*- coding: utf-8 -*-


from setuptools import setup
from dropbox_filemanager.version import __version__


install_requires = [
    'dropbox>=9.4.0'
    ]

setup(
    name='dropbox-filemanager',
    packages=['dropbox_filemanager'],
    scripts=['bin/dropbox-filemanager'],
    version=__version__,
    description="An application to manage files in dropbox account",
    long_description=open('README.md').read(),
    keywords=['file', 'manager', 'dropbox'],
    author="dslackw",
    author_email="d.zlatanidis@gamil.com",
    url="https://gitlab.com/dslackw/dropbox-filemanager",
    package_data={'': ['LICENSE.txt', 'README.md']},
    data_files=[('/var/lib/dropbox-filemanager', ['icons/icon.png',
                                                  'icons/logo.png'])],
    install_requires=install_requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: X11 Applications",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7"
        ],
    python_requires='>=3.7'
)
