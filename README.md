# Import Onboarding Bot

Telegram-бот для адаптации сотрудников кафе "Импорт".

## Возможности

- регистрация сотрудников;
- автоматическая рассылка учебных материалов;
- меню ресторана;
- тестирование;
- контакты сотрудников;
- административная панель.

## Стек технологий

- Python 3.13
- Aiogram 3
- SQLAlchemy
- SQLite (локально)
- PostgreSQL (production)
- APScheduler

## Запуск

```bash
pip install -r requirements.txt
python bot.py
```