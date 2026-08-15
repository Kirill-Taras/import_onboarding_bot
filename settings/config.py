"""
Загрузка конфигурации приложения.

Все настройки берутся из файла .env.
"""

from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    """Конфигурация приложения."""

    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///database/bot.db",
    )


settings = Settings()