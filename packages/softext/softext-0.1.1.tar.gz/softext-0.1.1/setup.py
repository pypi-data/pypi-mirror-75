# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['softext']

package_data = \
{'': ['*']}

install_requires = \
['Unidecode>=1.1.1,<2.0.0', 'nltk>=3.4.5,<4.0.0']

setup_kwargs = {
    'name': 'softext',
    'version': '0.1.1',
    'description': 'A package with some text cleaning tools',
    'long_description': None,
    'author': 'Aron Bordin',
    'author_email': 'aron.bordin@softplan.com.br',
    'maintainer': 'Luccas Quadros',
    'maintainer_email': 'luccas.quadros@softplan.com.br',
    'url': 'https://github.com/unj-inovacao/softext/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
