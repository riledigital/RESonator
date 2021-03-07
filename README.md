# RESonator Guide

## Installation

On Mac OS, run RESonator.app

# Development

- [Install pyenv](https://github.com/pyenv/pyenv) and use Python 3.7.10.

- [Install Poetry](https://python-poetry.org/docs/basic-usage/#project-setup) for
  dependency management. `poetry install` to install dependencies.

- Run `make build` which will auto clean the outputs.

- Run `make test` to run unit tests with `pytest`

If you run into issues with Pandas/Numpy/PyQt5, update pip to 21.x with `python -m pip install -U pip`. Poetry has issues installing PyQt5, so install that dependency manually with `pip` once you `poetry shell` to switch into the venv. Pyinstaller may output a bunch of errors about missing `dylib`s but the application should build successfully and run without issues. [May be fixable by building pyenv Python with headers?](https://github.com/pyenv/pyenv/issues/397)

The executable is placed in the ./dist folder. Run the binary to get a GUI and a console.
