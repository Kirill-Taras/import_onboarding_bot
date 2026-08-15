import asyncio

import models

from database.database import get_engine, init_db
from settings.config import settings


async def main() -> None:
    """
    Создаёт таблицы базы данных на основе зарегистрированных моделей.
    """
    engine = get_engine(settings.DATABASE_URL)

    await init_db(engine)

    await engine.dispose()

    print("✅ Таблицы базы данных успешно созданы.")


if __name__ == "__main__":
    asyncio.run(main())