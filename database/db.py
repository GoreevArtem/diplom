from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from setting.settings import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()


def get_db():
    with SessionLocal() as db:
        yield db
