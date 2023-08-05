# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cooperative_dataclasses']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'cooperative-dataclasses',
    'version': '0.2.2',
    'description': 'Cooperative dataclasses.',
    'long_description': '=======================\nCooperative Dataclasses\n=======================\n\n.. role:: bash(code)\n    :language: bash\n\n.. role:: python(code)\n   :language: python\n\nThis repository provides a version of dataclasses that can be used in\ncooperative inheritance.\n',
    'author': 'Neil Girdhar',
    'author_email': 'mistersheik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/NeilGirdhar/cooperative_dataclasses',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
