FROM python:3.13.0

RUN apt-get update && apt-get install -y curl

ENV POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.4

RUN mkdir /app

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.4

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY alembic.ini .

RUN poetry install --only=main --no-interaction --no-ansi

COPY /bot ./bot

RUN chmod +x ./bot/start.sh

CMD ["/app/bot/start.sh"]