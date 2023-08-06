# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['subtitle_sync',
 'subtitle_sync.utils',
 'subtitle_sync.utils.getMatchingDistinctWords',
 'subtitle_sync.utils.getMatchingDistinctWords.searchAlgorithms']

package_data = \
{'': ['*']}

install_requires = \
['Scrapy>=2.0.1,<3.0.0',
 'autopep8>=1.5.3,<2.0.0',
 'black>=19.10b0,<20.0',
 'flake8>=3.8.3,<4.0.0',
 'matplotlib>=3.2.2,<4.0.0',
 'num2words>=0.5.10,<0.6.0',
 'numpy>=1.19.0,<2.0.0',
 'pep8>=1.7.1,<2.0.0',
 'pylint>=2.5.3,<3.0.0',
 'pysbd>=0.2.3,<0.3.0',
 'rope>=0.17.0,<0.18.0',
 'spacy>=2.2.4,<3.0.0',
 'srt>=3.0.0,<4.0.0',
 'strsimpy>=0.1.7,<0.2.0',
 'subliminal>=2.0.5,<3.0.0',
 'tensorflow-gpu>=2.2.0,<3.0.0',
 'tensorflow>=2.2.0,<3.0.0',
 'tensorflow_hub>=0.8.0,<0.9.0',
 'unidecode>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'subtitle-sync',
    'version': '0.2.8',
    'description': '',
    'long_description': None,
    'author': 'VVNoodle',
    'author_email': 'brickkace@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
