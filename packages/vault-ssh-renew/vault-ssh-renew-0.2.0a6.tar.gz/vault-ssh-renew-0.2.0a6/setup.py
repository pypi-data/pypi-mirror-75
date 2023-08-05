# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vault_ssh_renew']

package_data = \
{'': ['*']}

install_requires = \
['click>=6.6,<7.0', 'paramiko>=2.7.1,<3.0.0', 'requests>=2.12.4,<3.0.0']

entry_points = \
{'console_scripts': ['vault-ssh-renew = vault_ssh_renew.cli:renew']}

setup_kwargs = {
    'name': 'vault-ssh-renew',
    'version': '0.2.0a6',
    'description': 'Vault SSH Host Key Renewal Tool',
    'long_description': None,
    'author': 'Niels Grewe',
    'author_email': 'niels.grewe@halbordnung.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
