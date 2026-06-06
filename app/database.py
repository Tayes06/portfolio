from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# Use aiosqlite for SQLite, asyncpg for PostgreSQL
if "sqlite" in settings.database_url:
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_async_engine(settings.database_url, echo=settings.debug, connect_args=connect_args)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    async with engine.begin() as conn:
        from app.models import contact, cv
        await conn.run_sync(Base.metadata.create_all)
