#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@author: rainsty
@file:   setup.py
@time:   2019-12-29 10:30:29
@description:
"""


try:
    from setuptools import setup
except BaseException as e:
    print(e)
    from distutils.core import setup


with open("README.md", "r") as fh:
        long_description = fh.read()


setup(
    name='pyrainsty',
    version='0.0.10',
    author='Residual Mark',
    author_email='1285679912@qq.com',
    description='The toolset.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/Rainstyed/pyrainsty',
    packages=['pyrainsty'],
    install_requires=[
        'requests>=2.22.0',
        'pymysql>=0.9.3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5'
)
