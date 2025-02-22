from app.config import get_db_url
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(engine, expire_on_commit=False)
