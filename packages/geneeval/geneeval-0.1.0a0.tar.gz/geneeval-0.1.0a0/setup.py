# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geneeval', 'geneeval.common']

package_data = \
{'': ['*']}

install_requires = \
['overrides>=3.1.0,<4.0.0',
 'pandas>=1.1.0,<2.0.0',
 'skorch>=0.8.0,<0.9.0',
 'typer[all]>=0.3.1,<0.4.0']

entry_points = \
{'console_scripts': ['geneeval = geneeval.main:app']}

setup_kwargs = {
    'name': 'geneeval',
    'version': '0.1.0a0',
    'description': 'A Python library for evaluating gene embeddings',
    'long_description': '![build](https://github.com/BaderLab/GeneEval/workflows/build/badge.svg)\n\n# GeneEval',
    'author': 'johngiorgi',
    'author_email': 'johnmgiorgi@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/BaderLab/GeneEval',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
