"""
Модель учебного материала.

Материал содержит название, описание
и ссылку на обучающий ресурс.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class Material(Base):
    """
    Модель учебного материала.

    Используется для хранения материалов,
    которые сотрудники получают через Telegram-бота.
    """

    __tablename__ = "materials"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    url: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )