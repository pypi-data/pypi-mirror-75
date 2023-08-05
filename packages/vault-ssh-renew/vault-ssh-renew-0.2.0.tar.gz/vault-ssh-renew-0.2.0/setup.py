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
    'version': '0.2.0',
    'description': 'Vault SSH Host Key Renewal Tool',
    'long_description': '# Vault SSH Renewal Tool\n\n[![Build Status](https://dev.azure.com/glaux/update-broker/_apis/build/status/ngrewe.vault-ssh-renew?branchName=master)](https://dev.azure.com/glaux/update-broker/_build/latest?definitionId=6&branchName=master)\n[![PyPI version](https://badge.fury.io/py/vault-ssh-renew.svg)](https://badge.fury.io/py/vault-ssh-renew)\n[ ![Download](https://api.bintray.com/packages/glaux/production/vault-ssh-renew/images/download.svg) ](https://bintray.com/glaux/production/vault-ssh-renew/_latestVersion)\n\n`vault-ssh-renew` automates the process of renewing SSH host certificates issued by\n[HashiCorp Vault](https://www.vaultproject.io/). It will check whether a certificate\nis installed on the host, and whether it expires in the near future. Only then will it\nrequest Vault to issue a new certificate.\n\nPlease note that `vault-ssh-renew` does not take care of renewing the Vault token itself or of re-configuring your SSH server software to actually present the certificate. Please refer to the\n[Vault documentation](https://www.vaultproject.io/docs/secrets/ssh/signed-ssh-certificates#host-key-signing) on how to achieve this.\n\n## Installation\n\n### Pip\n\n```sh\npip install vault-ssh-renew\n```\n\n### Debian/Ubuntu Packages\n\nOn Debian Buster, Ubuntu 18.04, and 20.04, you can install vault-ssh-renew from packages:\n\n```sh\nsudo apt-key adv --keyserver keyserver.ubuntu.com --recv AF0E925C4504784BF4E0FFF0C90E4BD2B36E75B9\necho "deb https://dl.bintray.com/glaux/production $(lsb_release -s -c) main" | sudo tee -a /etc/apt/sources.list.d/vault-ssh-renew.list\nsudo apt-get update\nsudo apt-get install vault-ssh-renew\n```\nThe package will also install a daily timer to run vault-ssh-renew. If you are installing interactively,\nyou will also be asked supply all the required configuration parameters, which will be written \nto `/etc/default/vault-ssh-renew` and can be edited there.\n\n### Docker\n\nYou may also run the tool using a Docker container:\n\n```\ndocker run -ti -v/etc/ssh:/etc/ssh \\\n    -e VAULT_TOKEN=**** \\\n    -e VAULT_ADDR=http://127.0.0.1:8200 \\\n    -e VAULT_SSH_SIGN_PATH=ssh/sign/host \\\n    glaux/vault-ssh-renew\n```\n\nFor every release, there also exists a corresponding tag suffixed with `.cron` (e.g.: `:latest.cron`) that\nruns the tools as a periodic cron job.\n\n## Configuration\n\nConfiguration can be achieved using the following environment variables.\n\n| Variable                           | Data Type       | Meaning | Default |\n|------------------------------------|-----------------|---------|---------|\n| `VAULT_ADDR`                       | URL             | Address under which Vault can be reached. | http://127.0.0.1:8200 |\n| `VAULT_TOKEN`                      | String          | Token for authentication against Vault. | |\n| `VAULT_TOKEN_FILE`                 | String          | The path to read the Vault token from. | |\n| `VAULT_SSH_HOST_KEY_PATH`          | String          | The path to the SSH public key. | `/etc/ssh/ssh_host_rsa_key.pub` |\n| `VAULT SSH_HOST_CERT_PATH`         | String          | The path to the SSH host certificate. | `/etc/ssh/ssh_host_rsa_key-cert.pub` |\n| `VAULT_SSH_SIGN_PATH`              | String          | The path to the signing endpoint, usually ⟨secret mountpoint⟩/sign/⟨role name⟩. |\n| `VAULT_SSH_PRINCIPALS`             | List of Strings | A space separated list of principals to request in the certificate | Host\'s FQDN |\n| `VAULT_SSH_RENEWAL_THRESHOLD_DAYS` | Integer         | When the certificate is valid for less then this many days, renew it. | 7 |\n\n\n## Kubernetes Deployment\n\nThe directory `kubernetes/` in the source distribution contains a set of resources that can serve as a template to deploy vault-ssh-renew across your Kubernetes cluster. You\'ll need to:\n\n* edit `secret.yaml` to supply your Vault token\n* add the correct Vault address and signing path to `configmap.yaml`\n* optionally change the version in `daemonset.yaml` to something other than `latest`\n\n```sh\nkubectl apply -f kubernetes/*.yaml\n```',
    'author': 'Niels Grewe',
    'author_email': 'niels.grewe@halbordnung.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ngrewe/vault-ssh-renew',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
