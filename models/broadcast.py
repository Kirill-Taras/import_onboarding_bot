"""
Модель рассылки.

Хранит информацию о сообщениях,
созданных администратором для сотрудников.
"""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class Broadcast(Base):
    """
    Модель рассылки.

    Хранит администратора, которому принадлежит рассылка,
    целевую группу сотрудников и текст сообщения.
    """

    __tablename__ = "broadcasts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    admin_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False,
    )

    target: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    message_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )