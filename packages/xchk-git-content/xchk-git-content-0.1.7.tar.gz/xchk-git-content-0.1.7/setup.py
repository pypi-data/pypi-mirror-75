# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['xchk_git_content', 'xchk_git_content.migrations']

package_data = \
{'': ['*'],
 'xchk_git_content': ['static/images/*', 'templates/xchk_git_content/*']}

install_requires = \
['xchk-regex-strategies>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'xchk-git-content',
    'version': '0.1.7',
    'description': 'Course material related to Git for the xchk teaching framework',
    'long_description': None,
    'author': 'Vincent Nys',
    'author_email': 'vincentnys@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
