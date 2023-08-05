# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plzpy']

package_data = \
{'': ['*']}

install_requires = \
['flask-cors>=3.0.8,<4.0.0', 'flask>=1.1.2,<2.0.0', 'waitress>=1.4.4,<2.0.0']

entry_points = \
{'console_scripts': ['plzpy = plzpy.plzpy:main']}

setup_kwargs = {
    'name': 'plzpy',
    'version': '0.1.0a0',
    'description': 'zip/buildings rest API for Berlin',
    'long_description': '# PLZ Rest API\n\nA simple rest API that exposes data related to zip codes and buildings in Berlin.\n\nThis project is the Python implementation of [PLZ](https://github.com/noandrea/plz)\n\nThe source dataset is published by [Esri](https://www.esri.de/de-de/home) \nand is available [here](https://opendata-esri-de.opendata.arcgis.com/datasets/273bf4ae7f6a460fbf3000d73f7b2f76_0).\n\n## Motivations\n\nBuilt as an exercise\n\n## Rest API\n\nPLZ provides the following endpoints:\n\n- `/status` returns the status of the service\n- `/zip/buildings` returns the number of buildings aggregated by zip code\n- `/zip/buildings/history` returns the number of buildings aggregated by zip code and year\n- `/zip/buildings/:code` returns the number of buildings for a specific zip code\n- `/zip/buildings/:code/history` returns the number of buildings aggregated by zip code and year for a specific zip code\n\n## Usage\n\nThere are 2 ways to run the PLZ api service: using Docker(recommended) or via [manual setup](#manual-setup).\n\nFor best results with Docker please use the image from the go project as described [here](https://github.com/noandrea/plz#docker) since the image is orders of magnitude smaller.\n\n\n### Manual setup\n\nThose are the steps to run the project manually:\n\n1. Install the library\n\n```\npip install plzpy\n```\n\n\n1. Download the dataset linked above:\n\n```sh\ncurl -L https://opendata.arcgis.com/datasets/273bf4ae7f6a460fbf3000d73f7b2f76_0.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D -o /tmp/src.csv\n```\n\n2. Massage the dataset to produce an optimized json to be served via the Rest API\n\n```sh\nplzpy massage --in /tmp/src.csv --out rest.json\n```\n\n3. Run the Rest API service\n\n```sh\nplzpy serve --data rest.json\n```\n\n',
    'author': 'Andrea Giacobino',
    'author_email': 'no.andrea@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/noandrea/plzpy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
