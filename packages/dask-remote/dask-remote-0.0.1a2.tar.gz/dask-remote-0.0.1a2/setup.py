# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dask_remote',
 'dask_remote.client',
 'dask_remote.deployment',
 'dask_remote.runner']

package_data = \
{'': ['*']}

install_requires = \
['distributed>=2.21.0,<3.0.0', 'requests', 'typing_extensions']

extras_require = \
{'deployment': ['kubernetes_asyncio>=10.0,<11.0'],
 'runner': ['fastapi', 'uvicorn']}

setup_kwargs = {
    'name': 'dask-remote',
    'version': '0.0.1a2',
    'description': 'Dask cluster based on a Kubernetes-native Deployment',
    'long_description': None,
    'author': 'Octopus Energy',
    'author_email': 'tech@octopus.energy',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/octoenergy/dask-remote',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
