# Сборочный образ
FROM python:3.13.0-slim-bullseye AS compile-image

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Переменные окружения для Python и Poetry
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    POETRY_VERSION=1.8.4

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 - --version 1.8.4

# Добавляем Poetry в PATH
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

# Установка только production зависимостей
RUN poetry install --only=main --no-interaction --no-ansi && \
    rm -rf $POETRY_CACHE_DIR

# Окончательный образ
FROM python:3.13.0-slim-bullseye

# Переменные окружения для Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем виртуальное окружение из сборочного образа
COPY --from=compile-image /app/.venv /app/.venv

# Добавляем виртуальное окружение в PATH
ENV PATH="/app/.venv/bin:$PATH"

# Копируем файлы проекта
COPY alembic.ini .
COPY ./bot ./bot

# Делаем стартовый скрипт исполняемым
RUN chmod +x ./bot/start.sh

# Добавляем пользователя с ограниченными правами
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Меняем пользователя
USER appuser

# Запуск стартового скрипта
CMD ["/app/bot/start.sh"]