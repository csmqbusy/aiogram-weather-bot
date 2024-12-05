FROM python:3.13.0-slim-bullseye

RUN apt-get update && apt-get install -y curl

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.4
ENV PATH="/app/.venv/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.4

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY alembic.ini .

RUN poetry install --only=main --no-interaction --no-ansi

COPY ./bot ./bot

RUN chmod +x ./bot/start.sh

CMD [ "/app/bot/start.sh" ]