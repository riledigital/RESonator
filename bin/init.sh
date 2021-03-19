#!/bin/sh
set -e
# install pyenv and dependencies for that
brew install pyenv openssl readline sqlite3 xz zlib
echo "Please set up your shell for pyenv... see the pyenv docs for instructions specific to your OS+shell."
pyenv install 3.7.10
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
poetry install
