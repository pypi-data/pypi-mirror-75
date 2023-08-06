# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docoseco']

package_data = \
{'': ['*']}

install_requires = \
['ruamel.yaml>=0.16.10,<0.17.0']

entry_points = \
{'console_scripts': ['docoseco = docoseco:main']}

setup_kwargs = {
    'name': 'docoseco',
    'version': '1.0.0',
    'description': 'Automatize management of docker confgs and secrets ',
    'long_description': '# Docoseco\n\n**Do**cker-**co**mpose **se**crets and **co**nfigs.\n\nAutomatize management of docker confgs and secrets.\n\n## Usage\n\n```\ndocoseco [CONFIG_ROOT_DIR] < docker-compose.template.yaml > docker-compose.yaml\n\n  CONFIG_ROOT_DIR  Root directory for file search (default: .)\n```\n\nIt reads docker-compose yaml from stdin, updates all config and secret names with corresponding file content hashsums and writes result to stdout.\n\n## Rationale\n\nDocker-compose configs and secrets are immutable by design. So, when config or secret is created from file via\n`docker stack deploy`, it\'s impossible to update the file and deploy in the same way again. For example:\n\n```yaml\n# docker-compose.yaml\nversion: "3.8"\nservices:\n  redis:\n    image: redis:latest\n    configs:\n      - source: my_config\n        target: /redis_config\nconfigs:\n  my_config:\n    file: ./my_config.txt\n```\n\nIf, after the initial deployment, `my_config.txt` is changed, the next deployment attempt will fail.\n\nThe common workaround is creating a new config, when a source file changes.\nThis is done by changing config name:\n\n```yaml\n# docker-compose.yaml\n...\nconfigs:\n  my_config:\n    name: my_config-2     # Changing name creates new docker config\n    file: ./my_config.txt # This file was changed\n```\n\nTo avoid manual management of config names, numerical suffix might be replaced by a file content hashsum, which can be automatically calculated.\n\n```yaml\n# docker-compose.yaml\n...\nconfigs:\n  my_config:\n    name: my_config-bee414b86ee02806b17104813d44eea4 # Auto-generated config name\n    file: ./my_config.txt # This file was changed\n```\n\n',
    'author': 'German Lashevich',
    'author_email': 'german.lashevich@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Zebradil/docoseco',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
