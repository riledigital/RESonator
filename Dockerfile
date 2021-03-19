FROM python:3.7.10-buster

WORKDIR /app
COPY ./poetry.lock .
COPY ./pyproject.toml .
COPY ./bin/init-docker.sh ./bin/
ENV POETRY_HOME="/usr/local/poetry"
# RUN ["/bin/bash", "./bin/init-docker.sh"]
# ENV PATH="${PATH}:/usr/local/poetry/bin"
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
