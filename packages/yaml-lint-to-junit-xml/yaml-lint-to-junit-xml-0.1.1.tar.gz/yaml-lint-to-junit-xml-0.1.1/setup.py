#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open("README.md").read()

setup(
    name="yaml-lint-to-junit-xml",
    version="0.1.1",
    description="Convert yaml-lint outputs to a jUnit valid xml tests result file",
    long_description=readme,
    long_description_content_type='text/markdown',
    author="Denis Shipilov",
    author_email="shipilovds@gmail.com",
    url="https://github.com/shipilovds/yaml-lint-to-junit-xml",
    packages=["yamllinttojunitxml"],
    package_dir={"yaml-lint-to-junit-xml": "yamllinttojunitxml"},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "yaml-lint-to-junit-xml = yamllinttojunitxml.yamllinttojunitxml:main"
        ]
    },
    install_requires=[],
    license="MIT",
    zip_safe=False,
    keywords=["yaml", "lint", "junit", "report"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: PyPy",
    ],
)
