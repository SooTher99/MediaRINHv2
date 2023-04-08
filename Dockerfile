FROM python:3.11.2-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

ENV POETRY_HOME /opt/poetry
RUN python3 -m venv $POETRY_HOME && $POETRY_HOME/bin/pip install poetry==1.4.2
ENV POETRY_BIN $POETRY_HOME/bin/poetry
COPY pyproject.toml poetry.lock ./

RUN $POETRY_BIN config --local virtualenvs.create false && $POETRY_BIN install --no-root

COPY . /app
