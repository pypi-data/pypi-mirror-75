# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['crisprbuilder_tb']

package_data = \
{'': ['*'], 'crisprbuilder_tb': ['data/*', 'doc/*', 'doc/.ipynb_checkpoints/*']}

install_requires = \
['biopython>=1.77,<2.0',
 'parallel-fastq-dump>=0.6.5,<0.7.0',
 'xlrd>=1.2.0,<2.0.0',
 'xmltodict>=0.12.0,<0.13.0']

setup_kwargs = {
    'name': 'crisprbuilder-tb',
    'version': '0.1.41',
    'description': 'Collect and annotate Mycobacterium tuberculosis WGS data for CRISPR investigations.',
    'long_description': '# CRISPRbuilder_TB\n------------------\n\n>This **README.md** gives you the gist of the CRISPRbuilder_TB package. Please refer to **crisprbuilder_tb.md** included in the package for more detailed explanation.    \n\n\n## Purpose of this package\n--------------------------\n\n>Collect and annotate Mycobacterium tuberculosis whole genome sequencing data for CRISPR investigation.    \n\n\n## Requirements\n---------------\n\n>CRISPRbuilder_TB needs the following dependencies to work:\n\n* python >= "3.6"\n* xlrd >= "1.2.0"\n* xmltodict >= "0.12.0"\n* biopython >= "1.77"\n\n>These different versions are automatically downloaded when installing the CRISPRbuilder_TB package.    \n\n\n## Installation\n---------------\n\n>Install the package by writing in the command prompt: `pip3 install crisprbuilder_tb`.    \n\n\n## How to use this package\n--------------------------\n\n>The most often common instruction for this package is: `python -m crisprbuilder_tb --collect {SRA_reference}`.\n\nSee the attached **criprbuilder-tb.md** for a comprehensive explanation.    \n\n\n## History\n----------\n\nFirst version of this package, which is 1.0.0 was published on July 2020.\n',
    'author': 'stephane-robin',
    'author_email': 'robin.stephane@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stephane-robin/crisprbuilder_tb.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
