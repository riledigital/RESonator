# RESonator Guide

## Installation

On Mac OS, unzip the tar.gz file to somewhere like `/Applications`, then run the `resonator-web-gui/resonator-web-gui` binary file. A console window will open and your web browser will launch the RESonator front-end. Quit the Terminal window to close the application.

RESonator currently requires an internet connection to display the Web frontend properly, since it depends on a CDN-hosted version of <a href="https://getbootstrap.com">Bootstrap</a>.

# Development

- [Install pyenv](https://github.com/pyenv/pyenv) and use Python 3.7.10.

- [Install Poetry](https://python-poetry.org/docs/basic-usage/#project-setup) for
  dependency management. `poetry install` to install dependencies.

- Run `make setup` to auto-install dev environment for Mac OS.

- Run `make freeze-cli` to build and freeze a cli executable binary to `./dist`.

- Run `make test` to run unit tests with `pytest`

If you run into issues with Pandas/Numpy/PyQt5, update pip to 21.x with `python -m pip install -U pip`. Poetry has issues installing PyQt5, so install that dependency manually with `pip` once you `poetry shell` to switch into the venv. Pyinstaller may output a bunch of errors about missing `dylib`s but the application should build successfully and run without issues. [May be fixable by building pyenv Python with headers?](https://github.com/pyenv/pyenv/issues/397)

The executable is placed in the ./dist folder. Run the binary to get a GUI and a console.

## Testing the CLI

Run the CLI with `poetry run cli` (configured through [pyproject.toml](https://dev.to/bowmanjd/build-a-command-line-interface-with-python-poetry-and-click-1f5k)).

## Web server

Test the web server by running `make serve`
