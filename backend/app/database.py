import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres")

environment_debug = os.getenv("DEBUG") == "1"
engine = create_engine(DATABASE_URL, echo=environment_debug)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
