# Crypto Tracker Bot

Telegram-бот для отслеживания курсов криптовалют, новостей и активности крупных игроков.

## Возможности

*   ✅ Получение актуальной цены по тикеру 
*   ⏳ Последние новости из мира крипты 
*   🔔 Подписка на уведомления (в разработке)
*   🐋 Отслеживание кошельков китов (в разработке)

## Технологии

*   Python 3.13+
*   Библиотека для Telegram Bot API: Aiogram 
*   Парсинг: Requests и bs4 (для работы с API)
*   HTTP-клиент: aiohttp
*   Хранение данных: PostgreSQL

## Установка и запуск

1.  Клонируйте репозиторий:
    ```bash
    git clone https://github.com/your_username/crypto-tracker-bot.git
    cd crypto-tracker-bot
    ```
2.  Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```
3.  Создайте файл `.env` и добавьте туда ваш Telegram Bot Token:
    ```ini
    TG_TOKEN=your_bot_token_here
    ```
4.  Запустите бота:
    ```bash
    python run.py
    ```

## contributing

Если у вас есть предложения по улучшению — welcome! Форкните репозиторий, создайте ветку для вашей фичи, сделайте pull request.