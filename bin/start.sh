#!/usr/bin/env
echo "Gunicorn running RESonator web app:" &&
    poetry run gunicorn resonator.web.app:app
