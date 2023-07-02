from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser
from pathlib import Path


config = configparser.ConfigParser()
config.read("config.ini")

DB_NAME = config.get("DATABASE", "db_name") 
current_dir = Path(__file__).resolve().parent
# Construct the connection string using the absolute path
CONN_STRING = f"sqlite:///{current_dir / DB_NAME}"

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

engine = create_engine(CONN_STRING)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
