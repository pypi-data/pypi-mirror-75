# python-openevse-wifi
A python library for communicating with the ESP8266- and ESP32-based wifi module from OpenEVSE.
This library uses RAPI commands over http to query the OpenEVSE charger.

Currently only supports read-only functionality.

## Installation
The easiest way of installing the latest stable version is with pip:
```
pip install openevsewifi
```
This project uses poetry for dependency management and package publishing.  To install from source using poetry:
```
poetry install
```
If you're not planning on doing any development on python-openevse-wifi itself, and you don't want to install poetry, 
you can also use pip as of version 10.0.  From the root of this repo, run:
```
pip install .
```

## Development
To set up a development environment, first install Poetry according to the 
[directions](https://python-poetry.org/docs/).
Then install the dependencies for this project:
```
poetry install
```
Before opening a pull request, make sure all tests pass by running `pytest`.
