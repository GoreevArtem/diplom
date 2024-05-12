from fastapi import FastAPI

import api
from database.db import engine
from database.models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(api.router)
