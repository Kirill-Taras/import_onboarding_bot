"""
Точка входа в приложение.
"""

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from settings.config import settings

bot = Bot(settings.BOT_TOKEN)

storage = MemoryStorage()

dp = Dispatcher(storage=storage)