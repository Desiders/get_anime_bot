from app.config import Database
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


def make_connection_string(
    database: Database,
    async_fallback: bool = False,
) -> str:
    return (
        "postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"
        "?async_fallback={async_fallback}"
    ).format(
        user=database.user, password=database.password,
        host=database.host, port=database.port,
        name=database.name, async_fallback=async_fallback,
    )


def sa_sessionmaker(
    connection_string: str,
    echo: bool = False,
) -> sessionmaker:
    return sessionmaker(
        bind=create_async_engine(connection_string, echo=echo, pool_size=20),
        expire_on_commit=False, class_=AsyncSession,
        future=True, autoflush=False,
    )
