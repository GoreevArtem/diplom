import os
import dotenv

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("db")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()


def get_db():
    with SessionLocal() as db:
        yield db
