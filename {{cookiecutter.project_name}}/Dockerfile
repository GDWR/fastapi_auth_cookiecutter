FROM python:3.8

ARG POETRY_VERSION=1.1.12
WORKDIR /app

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -

# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN $HOME/.poetry/bin/poetry config virtualenvs.create false \
    && $HOME/.poetry/bin/poetry install --no-dev --no-interaction --no-ansi

# Copy source
COPY {{cookiecutter.project_name}} .
