from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession, async_sessionmaker
from core.configs import settings

engine: AsyncEngine = create_async_engine(
    settings.DB_URL,
    echo=False,
    future=True
)

SessionLocal: AsyncSession = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    autoflush=False,
    autocommit=False,
    class_=AsyncSession
)

