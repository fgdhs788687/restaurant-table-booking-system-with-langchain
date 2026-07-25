from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# The Engine which connects with the database:
engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True
)

# AsyncSessionLocal is a fcatory that creates session
AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)

# Creating Base for db tables:
Base = declarative_base()

# This function is used to create a session:
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session