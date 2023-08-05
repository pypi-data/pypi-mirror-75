import os
import sys
from setuptools import setup, Extension

# https://packaging.python.org/guides/making-a-pypi-friendly-readme/
# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()



# How python packaging recommends storing the version
import codecs
import os.path

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")





setup(name='iterprinter',
	version=get_version("iterprinter/__init__.py"),
	description = 'An iteration history printer',
	long_description=long_description,
	long_description_content_type='text/markdown',
	author = 'Jeffrey M. Hokanson',
	packages = ['iterprinter'],
	install_requires = [],
	zip_safe = False,
)
