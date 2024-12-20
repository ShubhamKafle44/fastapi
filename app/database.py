import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
load_dotenv()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DATABASE_PASSKEY = os.getenv("DATABASE_PASSKEY")
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSKEY}@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal =  sessionmaker(autocommit= False, autoflush=False, bind =engine)

Base =  declarative_base()