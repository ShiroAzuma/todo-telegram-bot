# Todo Telegram Bot

Телеграм-бот для управления списком задач.

## Функциональность

- Добавление задач
- Просмотр списка задач
- Отметка задачи как выполненной
- Удаление задачи

## Зависимости

- Python 3.9+
- aiogram 3.x
- python-dotenv

## Установка и запуск

1. Клонировать репозиторий:
git clone https://github.com/ShiroAzuma/todo-telegram-bot.git
cd todo-telegram-bot

2. Создать виртуальное окружение:
python3 -m venv venv
source venv/bin/activate

3. Установить зависимости:
pip install -r requirements.txt

4. Создать файл .env и добавить токен:
BOT_TOKEN=ваш_токен

5. Запустить бота:
export $(cat .env) && python3 bot.py
