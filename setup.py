#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup configuration for Caselaw Fact-Checker
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name='caselaw-factchek',
    version='1.0.0',
    description='Legal Fact-Checking System for Cyprus Bankruptcy Law',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='nvoskos',
    author_email='',
    url='https://github.com/nvoskos/caselaw-factchek',
    packages=find_packages(exclude=['tests', 'outputs']),
    include_package_data=True,
    install_requires=[
        'networkx>=3.0',
        'matplotlib>=3.7.0',
        'click>=8.1.0',
        'python-dateutil>=2.8.0',
    ],
    extras_require={
        'dev':  [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'pylint>=2.17.0',
        ],
        'viz': [
            'pygraphviz>=1.11',
        ]
    },
    entry_points={
        'console_scripts':  [
            'bankruptcy-factcheck=bankruptcy_factcheck: main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Legal Industry',
        'Topic :: Software Development :: Libraries ::  Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Natural Language :: Greek',
        'Natural Language :: English',
    ],
    python_requires='>=3.9',
    keywords='legal fact-checking bankruptcy cyprus law interpretation',
)