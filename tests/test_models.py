"""
Тесты моделей базы данных.

Проверяем:
- регистрацию моделей в Base.metadata;
- создание таблиц;
- создание и чтение Employee;
- создание и чтение Material;
- создание Broadcast с внешним ключом на Employee.
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

import models

from database.database import Base
from models.broadcast import Broadcast
from models.employee import Employee
from models.material import Material


@pytest_asyncio.fixture
async def session() -> AsyncSession:
    """
    Создаёт тестовую SQLite-базу в памяти.

    Для каждого теста создаётся отдельный engine.
    StaticPool позволяет использовать одно соединение
    с SQLite :memory:, поэтому таблицы остаются доступными
    во время всего теста.
    """

    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={
            "check_same_thread": False,
        },
        poolclass=StaticPool,
    )

    # Создаём таблицы.
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    # Создаём сессию.
    async with AsyncSession(engine) as session:
        yield session

    # После теста закрываем engine.
    await engine.dispose()


def test_models_registered() -> None:
    """
    Проверяет, что все модели зарегистрированы
    в Base.metadata.
    """

    tables = Base.metadata.tables

    assert "employees" in tables
    assert "materials" in tables
    assert "broadcasts" in tables


@pytest.mark.asyncio
async def test_create_employee(session: AsyncSession) -> None:
    """
    Проверяет создание сотрудника
    и сохранение его в базе данных.
    """

    employee = Employee(
        telegram_id=123456789,
        username="test_user",
        full_name="Иван Иванов",
        phone="+79990000000",
        position="Официант",
    )

    session.add(employee)
    await session.commit()

    result = await session.execute(
        select(Employee).where(
            Employee.telegram_id == 123456789
        )
    )

    saved_employee = result.scalar_one()

    assert saved_employee.full_name == "Иван Иванов"
    assert saved_employee.username == "test_user"
    assert saved_employee.phone == "+79990000000"
    assert saved_employee.position == "Официант"
    assert saved_employee.role == "employee"
    assert saved_employee.status == "active"


@pytest.mark.asyncio
async def test_create_material(session: AsyncSession) -> None:
    """
    Проверяет создание учебного материала
    и сохранение его в базе данных.
    """

    material = Material(
        title="Стандарты сервиса",
        description="Основные стандарты работы с гостями.",
        url="https://example.com/service",
    )

    session.add(material)
    await session.commit()

    result = await session.execute(
        select(Material).where(
            Material.title == "Стандарты сервиса"
        )
    )

    saved_material = result.scalar_one()

    assert saved_material.title == "Стандарты сервиса"
    assert saved_material.description == (
        "Основные стандарты работы с гостями."
    )
    assert saved_material.url == "https://example.com/service"


@pytest.mark.asyncio
async def test_create_broadcast(
    session: AsyncSession,
) -> None:
    """
    Проверяет создание рассылки,
    связанной с существующим сотрудником.
    """

    employee = Employee(
        telegram_id=987654321,
        username="admin",
        full_name="Администратор Тестовый",
        position="Управляющий",
        role="admin",
    )

    session.add(employee)

    # flush отправляет INSERT в БД,
    # но не завершает транзакцию.
    # После flush SQLAlchemy уже знает employee.id.
    await session.flush()

    employee_id = employee.id

    broadcast = Broadcast(
        admin_id=employee_id,
        target="waiters",
        message_text="Завтра собрание в 10:00.",
    )

    session.add(broadcast)
    await session.commit()

    result = await session.execute(
        select(Broadcast).where(
            Broadcast.admin_id == employee_id
        )
    )

    saved_broadcast = result.scalar_one()

    assert saved_broadcast.admin_id == employee_id
    assert saved_broadcast.target == "waiters"
    assert saved_broadcast.message_text == (
        "Завтра собрание в 10:00."
    )