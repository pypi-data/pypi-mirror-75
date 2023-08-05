#!python
# coding=utf-8

__author__ = "Garrett Bates"
__copyright__ = "© Copyright 2020, Tartan Solutions, Inc"
__credits__ = ["Garrett Bates"]
__license__ = "Apache 2.0"
__version__ = "0.1.2"
__maintainer__ = "Garrett Bates"
__email__ = "garrett.bates@tartansolutions.com"
__status__ = "Development"

from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='docker-entrypoint',
    author='Garrett Bates, Dave Parsons',
    author_email='garrett.bates@tartansolutions.com, dave.parsons@tartansolutions.com',
    description="Basic utility to proxy a container's normal entrypoint",
    version='0.1.2',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/PlaidCloud/docker-entrypoint',
    keywords='container kubernetes debug development',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
    ],
    packages=find_packages(),
    install_requires=[
        'python-dotenv',
        'ptvsd',
        'pydevd-pycharm',
    ],
    entry_points='''
        [console_scripts]
        entrypoint=entrypoint.main:main
    ''',
    python_requires='>=3.7',
)
