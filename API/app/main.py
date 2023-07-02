from fastapi import FastAPI
import configparser
from .routes import polls

config = configparser.ConfigParser()
config.read("config.ini")

TITLE = config.get("APP", "title")
DESCRIPTION = config.get("APP", "description")

app = FastAPI(title=TITLE,
              description=DESCRIPTION)

app.include_router(polls.router)
#app.include_router(question.router) ...