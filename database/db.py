from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from service.recipe import PostSingleton
from setting.settings import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
print(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()

MONGO_URI = f"mongodb://mongo:27017"
post_singleton = PostSingleton(MONGO_URI)

def get_db():
    with SessionLocal() as db:
        yield db
