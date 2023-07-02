import uvicorn
import configparser
from app.main import app


config = configparser.ConfigParser()
config.read("config.ini")

PORT = int(config.get("APP", "port"))
HOST = config.get("APP", "host")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)