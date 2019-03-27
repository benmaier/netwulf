from setuptools import setup, Extension
import setuptools
import os, sys

# get __version__, __author__, and __email__
exec(open("./netwulf/metadata.py").read())

setup(
    name = 'netwulf',
    version = __version__,
    author = __author__,
    author_email = __email__,
    url = 'https://github.com/benmaier/netwulf',
    license = __license__,
    description = "Interactively visualize networks with Ulf Aslak's d3-tool from Python.",
    long_description = '',
    packages = setuptools.find_packages(),
    setup_requires = [
            ],
    install_requires = [
                'networkx>=2.0',
                'numpy>=0.14',
                'matplotlib>=3.0',
                'simplejson>=3.0',
            ],
    include_package_data = True,
    zip_safe = False,
)
