FROM python:3.11.0-slim AS development_build

ARG DJANGO_ENV

ENV DJANGO_ENV=${DJANGO_ENV} \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.4.2 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

# System deps:
RUN apt-get update && apt-get -y install gcc

# set work directory
WORKDIR /app

# Install dependencies:
RUN pip install poetry
ADD pyproject.toml poetry.lock /app/
RUN poetry config virtualenvs.create false && poetry config installer.max-workers 10
RUN poetry install --no-root
# RUN playwright install && playwright install-deps 

# copy project
COPY . .