#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-doctest-ufunc',
    version='0.1.3',
    author='Leo Singer',
    author_email='leo.singer@ligo.org',
    maintainer='Leo Singer',
    maintainer_email='leo.singer@ligo.org',
    license='MIT',
    url='https://github.com/lpsinger/pytest-doctest-ufunc',
    description='A plugin to run doctests in docstrings of Numpy ufuncs',
    long_description=read('README.rst'),
    py_modules=['pytest_doctest_ufunc'],
    python_requires='>=3.6',
    install_requires=['numpy', 'pytest>=3.5.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'doctest-ufunc = pytest_doctest_ufunc',
        ],
    },
)
