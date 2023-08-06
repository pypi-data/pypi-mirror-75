# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lospec2aseprite']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.1,<5.0.0',
 'progressbar2>=3.51.4,<4.0.0',
 'requests_download>=0.1.2,<0.2.0']

entry_points = \
{'console_scripts': ['lospec2aseprite = lospec2aseprite.importer:main']}

setup_kwargs = {
    'name': 'lospec2aseprite',
    'version': '0.1.0',
    'description': 'Import palettes from Lospec to Aseprite',
    'long_description': '# special-octo-bassoon\nImport a lospec palette into aseprite, personal use, feel free to read and modify this for your own needs\n\n## How to use\n`# import.py [url to 32x.png palette file from lospec]`\n',
    'author': 'Konosprod',
    'author_email': 'konosprod@free.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Konosprod/lospec2aseprite',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
