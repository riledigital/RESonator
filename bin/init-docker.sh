#/bin/bash
set -e

curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
# source $HOME/.poetry/env
poetry update
poetry install
