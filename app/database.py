from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

db_url = settings.database_url

# Normalize PostgreSQL URLs to use asyncpg driver
if db_url.startswith("postgres://") or db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)

# Use aiosqlite for SQLite, asyncpg for PostgreSQL
if "sqlite" in db_url:
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}

engine = create_async_engine(db_url, echo=settings.debug, connect_args=connect_args)
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
