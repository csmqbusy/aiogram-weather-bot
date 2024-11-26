## Описание

Это **пример Telegram-бота**, написанного с помощью **aiogram-dialog**. 
Бот позволяет пользователям получать текущую погоду по названию города. 
Поддерживает три способа запроса погоды: указание своего города и получение погоды в один клик, запрос погоды в другом городе и запрос погоды в случайном городе. Также можно просматривать историю своих запросов.

<img src="quick_demonstration.gif" width="420" height="430" />

### Технологии

- **aiogram**
- **aiogram-dialog**: Библиотека-расширение для aiogram, которая упрощает создание диалогов.
- **SQLAlchemy**

### Установка

1. Клонируйте репозиторий
2. Создайте виртуальное окружение и активируйте его
3. Установите зависимости из pyproject.toml
4. Переименуйте файл конфигурации `.env.example` в `.env` и заполните его своими данными
5. Используемое API для погоды – https://www.weatherapi.com/

6. Соберите docker-образы с помощью команды:
    ```shell
    docker compose build
    ```
7. Запустите контейнеры с ботом при помощи команды:
   ```shell
    docker compose up
    ```
