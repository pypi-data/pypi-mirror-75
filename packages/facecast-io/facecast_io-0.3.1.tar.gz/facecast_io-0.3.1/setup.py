# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['facecast_io', 'facecast_io.core']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.12.1,<0.13.0',
 'pyquery>=1.4.1,<2.0.0',
 'retry>=0.9.2,<0.10.0',
 'yarl>=1.4.2,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['typing>=3.7,<4.0', 'typing_extensions>=3.7,<4.0']}

setup_kwargs = {
    'name': 'facecast-io',
    'version': '0.3.1',
    'description': 'Unofficial API for facecast.io',
    'long_description': '***********\nFacecast IO\n***********\n\nUnofficial API client to https://facecast.io service\n####################################################\n\nInstallation\n************\n\n:pip: pip install facecast-io\n:poetry: poetry add facecast-io\n\nUsage\n*****\n\n::\n\n    api = FacecastAPI(os.environ["FACECAST_USERNAME"], os.environ["FACECAST_PASSWORD"])\n\n',
    'author': 'Serhii Khalymon',
    'author_email': 'sergiykhalimon@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/skhalymon/facecast-io',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
