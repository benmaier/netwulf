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
    python_requires='~=3.5', 
    install_requires = [
                'networkx>=2.0',
                'numpy>=0.14',
                'matplotlib>=3.0',
                'simplejson>=3.0',
            ],
    tests_require=['pytest', 'pytest-cov'],
    setup_requires=['pytest-runner'],
    classifiers=['License :: OSI Approved :: MIT License',
                'Programming Language :: Python :: 3.5',
                'Programming Language :: Python :: 3.6',
                'Programming Language :: Python :: 3.7'
               ],
    project_urls={
        'Documentation': 'https://netwulf.rtfd.io',
        'Contributing Statement': 'https://github.com/benmaier/netwulf/blob/master/CONTRIBUTING.md',
        'Bug Reports': 'https://github.com/benmaier/netwulf/issues',
        'Source': 'https://github.com/benmaier/netwulf/',
        'PyPI': 'https://pypi.org/project/netwulf/',
    },
    include_package_data = True,
    zip_safe = False,
)
