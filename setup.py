#This file is forked from https://github.com/pybind/pbtest, original author: Sylvain Corlay

from setuptools import setup, Extension
import setuptools
import os, sys

# get __version__, __author__, and __email__
exec(open("./netwulf/metadata.py").read())

setup(
    name = 'tacoma',
    version = __version__,
    author = __author__,
    author_email = __email__,
    url = 'https://github.com/benmaier/netwulf',
    license = __license__,
    description = "Interactively visualize networks with Ulf Aslak's d3-tool from Python."
    long_description = '',
    packages = setuptools.find_packages(),
    ext_modules = ext_modules,
    setup_requires = [
            ],
    install_requires = [
            ],
    include_package_data = True,
    zip_safe = False,
)
