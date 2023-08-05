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
    'version': '0.1.0',
    'description': 'zip/buildings rest API for Berlin',
    'long_description': "# PLZ Rest API\n\nA simple rest API that exposes data related to zip codes and buildings in Berlin.\n\nThis project is the Python implementation of [PLZ](https://github.com/noandrea/plz)\n\nThe source dataset is published by [Esri](https://www.esri.de/de-de/home) \nand is available [here](https://opendata-esri-de.opendata.arcgis.com/datasets/273bf4ae7f6a460fbf3000d73f7b2f76_0).\n\n## Motivations\n\nBuilt as an exercise\n\n## Rest API\n\nPLZ provides the following endpoints:\n\n- `/status` returns the status of the service\n- `/zip/buildings` returns the number of buildings aggregated by zip code\n- `/zip/buildings/history` returns the number of buildings aggregated by zip code and year\n- `/zip/buildings/:code` returns the number of buildings for a specific zip code\n- `/zip/buildings/:code/history` returns the number of buildings aggregated by zip code and year for a specific zip code\n\n## Usage\n\nThere are 2 ways to run the PLZ api service: using [Docker](#docker)(recommended) or via [manual setup](#manual-setup).\n\n### Docker\n\nThe Docker image is available at [noandrea/plz](https://hub.docker.com/repository/docker/noandrea/plz), and can be run with\n\n```sh\ndocker run -p 2007:2007 noandrea/plz\n```\n\nThe image is built on [scratch](https://hub.docker.com/_/scratch), the image size is ~9.3mb:\n\n[![asciicast](https://asciinema.org/a/350213.svg)](https://asciinema.org/a/350213)\n\n### Manual setup\n\nThere are 3 steps to setup the service:\n\n1. Download the dataset linked above:\n\n```sh\ncurl -L https://opendata.arcgis.com/datasets/273bf4ae7f6a460fbf3000d73f7b2f76_0.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D -o /tmp/src.csv\n```\n\n2. Massage the dataset to produce an optimized json to be served via the Rest API\n\n```sh\nplz massage --in /tmp/src.csv --out rest.json\n```\n\n3. Run the Rest API service\n\n```sh\nplz serve --data rest.json\n```\n\n[![asciicast](https://asciinema.org/a/350219.svg)](https://asciinema.org/a/350219)\n\n## Examples\n\n### Docker compose\n\n`docker-compose.yaml` example\n\n```yaml\nversion: '3'\nservices:\n  plz:\n    container_name: plz\n    image: noandrea/plz:latest\n    ports:\n    - 2007:2007\n\n```\n\n\n### K8s\n\nKubernetes configuration example:\n\n```yaml\n---\n# Deployment\napiVersion: extensions/v1beta1\nkind: Deployment\nmetadata:\n  labels:\n    app: plz\n  name: plz\nspec:\n  replicas: 1\n  revisionHistoryLimit: 3\n  selector:\n    matchLabels:\n      app: plz\n  template:\n    metadata:\n      labels:\n        app: plz\n    spec:\n      containers:\n      - env:\n        image: noandrea/plz:latest\n        imagePullPolicy: Always\n        name: plz\n        ports:\n        - name: http\n          containerPort: 2007\n        livenessProbe:\n          httpGet:\n            path: /status\n            port: 2007\n---\n# Service\n# the service for the above deployment\napiVersion: v1\nkind: Service\nmetadata:\n  name: plz-service\nspec:\n  type: ClusterIP\n  ports:\n  - name: http\n    port: 80\n    protocol: TCP\n    targetPort: http\n  selector:\n    app: plz\n\n```\n",
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
