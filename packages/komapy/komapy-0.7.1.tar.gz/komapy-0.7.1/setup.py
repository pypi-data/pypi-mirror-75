#!/usr/bin/env python

import os

from setuptools import setup, find_packages

__version__ = '0.7.1'


def read(filename):
    """Read file contents."""
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


setup(
    name='komapy',
    version=__version__,
    description='Python library for creating customizable BPPTKG Monitoring API chart',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    license='MIT',
    install_requires=[
        'matplotlib>=3.0.0',
        'pandas>=0.24,<1.1',
        'bmaclient>=0.6.0',
    ],
    author='Indra Rudianto',
    author_email='indrarudianto.official@gmail.com',
    url='https://gitlab.com/bpptkg/komapy',
    zip_safe=False,
    packages=find_packages(exclude=['docs', 'examples', 'tests']),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Operating System :: POSIX :: Linux',
        'Intended Audience :: Science/Research',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
