from setuptools import setup
import subprocess
import sys
import os


setup(
    name='aha-tools',
    version='0.0.1',
    author='Teguh Hofstee',
    author_email='thofstee@stanford.edu',
    url='https://github.com/StanfordAHA/aha',

    python_requires='>=3.7',
    install_requires = [
        'docker',
        'genesis2',
        'gitpython',
        'networkx',
        'packaging',
        'pydot',
        'requirements-parser',
        'tabulate',
    ],
    setup_requires = [
        'networkx',
        'packaging',
    ],

    entry_points = {
        'console_scripts': ['aha=aha.aha:main'],
    },
)
