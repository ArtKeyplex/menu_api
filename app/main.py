from fastapi import FastAPI

from . import models
from .database import engine
from .routers import menu


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(menu.router)
