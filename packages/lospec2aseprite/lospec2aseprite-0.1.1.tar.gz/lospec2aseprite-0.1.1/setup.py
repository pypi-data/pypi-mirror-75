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
    'version': '0.1.1',
    'description': 'Import palettes from Lospec to Aseprite',
    'long_description': '\n# lospec2aseprite\n\nImport a lospec palette into aseprite, personal use, feel free to read and modify this for your own needs\n\n## How to use\n\n`# lospec2aseprite [URL]`\n\nIt will automaticaly create an extension per author and add the palette. If several palettes for an author are added, it automatically update the extension. You have to restart Aseprite between adds.\n\n## How to install\n\n### Via `pip`\n\n`pip install lospec2aseprite`\n\n### Via the sources\n\n* `git clone https://github.com/Konosprod/lospec2aseprite.git`\n* `cd lospec2aseprite`\n* `poetry install`\n\n',
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
