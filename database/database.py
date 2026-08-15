"""
Настройка подключения к базе данных.

Модуль отвечает за:
- создание SQLAlchemy Base;
- создание асинхронного Engine;
- создание фабрики AsyncSession;
- безопасное получение и закрытие сессий;
- создание таблиц базы данных.
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Базовый класс для всех ORM-моделей проекта.

    Все модели SQLAlchemy должны наследоваться от этого класса.
    Например:

        class User(Base):
            ...
    """


def get_engine(
    database_url: str,
    *,
    echo: bool = False,
) -> AsyncEngine:
    """
    Создаёт асинхронный SQLAlchemy Engine.

    Args:
        database_url: URL подключения к базе данных.
        echo: Если True, SQLAlchemy выводит SQL-запросы в консоль.

    Returns:
        AsyncEngine: асинхронный движок SQLAlchemy.
    """
    return create_async_engine(
        database_url,
        echo=echo,
        poolclass=NullPool,
    )


def get_sessionmaker(
    engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    """
    Создаёт фабрику асинхронных сессий.

    Args:
        engine: асинхронный SQLAlchemy Engine.

    Returns:
        async_sessionmaker[AsyncSession]: фабрика для создания сессий.
    """
    return async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


@asynccontextmanager
async def get_session(
    session_factory: async_sessionmaker[AsyncSession],
) -> AsyncGenerator[AsyncSession, None]:
    """
    Предоставляет асинхронную сессию для работы с базой данных.

    Сессия автоматически закрывается после завершения блока
    `async with`.

    Args:
        session_factory: фабрика асинхронных сессий.

    Yields:
        AsyncSession: активная сессия SQLAlchemy.

    Example:
        async with get_session(session_factory) as session:
            result = await session.execute(...)
    """
    async with session_factory() as session:
        yield session


async def init_db(engine: AsyncEngine) -> None:
    """
    Создаёт все таблицы, зарегистрированные в Base.metadata.

    Перед вызовом функции необходимо импортировать все модели,
    чтобы SQLAlchemy знал об их существовании.

    Args:
        engine: асинхронный SQLAlchemy Engine.
    """
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def close_db(engine: AsyncEngine) -> None:
    """
    Закрывает соединения SQLAlchemy Engine.

    Args:
        engine: асинхронный SQLAlchemy Engine.
    """
    await engine.dispose()