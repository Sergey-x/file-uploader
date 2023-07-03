from sqlalchemy.ext.asyncio import AsyncSession

from file_uploader.db.db import MyDatabase


async def get_db() -> AsyncSession:
    MyDatabase.init()
    async with MyDatabase.async_session() as session:
        yield session
