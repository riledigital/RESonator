#!/bin/sh
# install pyenv and dependencies for that
brew install pyenv openssl readline sqlite3 xz zlib
pyenv install 3.7.10
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
