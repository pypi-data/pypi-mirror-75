#!/usr/bin/env python
from setuptools import setup, find_packages

def read_version():
    with open("VERSION.txt", mode='r') as version_file:
        version = version_file.read()
    return version



if __name__ == "__main__":
    setup(
        version=read_version(),
        packages=find_packages(exclude=["*tests*"])
    )