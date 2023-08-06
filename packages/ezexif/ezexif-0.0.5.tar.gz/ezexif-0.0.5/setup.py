#!/usr/bin/env python
# coding: utf-8

# python3 setup.py sdist
# twine upload dist/*

from setuptools import setup

setup(
    name='ezexif',
    version='0.0.5',
    author='wsgfz',
    author_email='wsgfz.cn@gmail.com',
    url='https://wsgfz.cn',
    description='Wrapper for origin exifread.process_file',
    packages=['ezexif'],
    install_requires=['ExifRead>=2.1.2, <=2.2.1']
)