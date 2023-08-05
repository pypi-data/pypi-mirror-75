# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['willing_zg', 'willing_zg.resources']

package_data = \
{'': ['*']}

install_requires = \
['zygoat>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'willing-zg',
    'version': '1.2.1',
    'description': '',
    'long_description': '# willing_zg\n\nWilling specific plugins for Zygoat\n\n<img src="https://user-images.githubusercontent.com/640862/81694571-7a08eb00-942f-11ea-87f9-c419cb4f8900.jpg" />\n\n## How does it work?\n\n`willing-zg` works by adding additional components for `zygoat` to use when installing or upgrading a repository. These are components that the Willing team wants in every application, but might not be appropriate for every `zygoat` application.\n\n## How do I use it?\n\nMake sure `zygoat` is installed. Then install `willing-zg`:\n\n```bash\npip install --user --upgrade /path/to/willing-zg\n```\n\nGo to your application directory and update the `zygoat_settings.yml` file to include the additional components.\n\n```\nextras:\n    - willing_zg:component_name\n    - willing_zg:other_component_name\n```\n\nThen run a zygoat update to install the new components.\n\n```bash\nzg update\n```\n',
    'author': 'Bequest, Inc.',
    'author_email': 'oss@willing.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
