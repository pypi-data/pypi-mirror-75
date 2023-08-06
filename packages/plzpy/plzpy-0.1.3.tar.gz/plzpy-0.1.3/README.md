# PLZ Rest API

A simple rest API that exposes data related to zip codes and buildings in Berlin.

> This project is the Python implementation of [PLZ](https://github.com/noandrea/plz)

The source dataset is published by [Esri](https://www.esri.de/de-de/home) 
and is available [here](https://opendata-esri-de.opendata.arcgis.com/datasets/273bf4ae7f6a460fbf3000d73f7b2f76_0).

## Motivations

Built as an exercise

## Rest API

PLZ provides the following endpoints:

- `/status` returns the status of the service
- `/zip/buildings` returns the number of buildings aggregated by zip code
- `/zip/buildings/history` returns the number of buildings aggregated by zip code and year
- `/zip/buildings/:code` returns the number of buildings for a specific zip code
- `/zip/buildings/:code/history` returns the number of buildings aggregated by zip code and year for a specific zip code

## Usage

There are 2 ways to run the PLZ api service: using Docker(recommended) or via [manual setup](#manual-setup).

For best results with Docker please use the image from the go project as described [here](https://github.com/noandrea/plz#docker) since the image is orders of magnitude smaller.


### Manual setup

Those are the steps to run the project manually:

1. Install the library

```
pip install plzpy
```


1. Download the dataset linked above:

```sh
curl -L https://opendata.arcgis.com/datasets/273bf4ae7f6a460fbf3000d73f7b2f76_0.csv?outSR=%7B%22latestWkid%22%3A3857%2C%22wkid%22%3A102100%7D -o /tmp/src.csv
```

2. Massage the dataset to produce an optimized json to be served via the Rest API

```sh
plzpy massage --in /tmp/src.csv --out rest.json
```

3. Run the Rest API service

```sh
plzpy serve --data rest.json
```

[![asciicast](https://asciinema.org/a/350289.svg)](https://asciinema.org/a/350289?t=57&autoplay=1)

## Development

The project relies on [poetry](https://python-poetry.org/).