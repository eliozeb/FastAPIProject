from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db(): # a function to get the database session from the dependency injection system of FastAPI 
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# documentation purposes only : the following commented code is for connecting to the database using psycopg2 
""" while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="saselias123",
            cursor_factory=RealDictCursor,
            port=5432
        )
        cursor = conn.cursor()
        print("Connected to the database")
        break
    except Exception as e:
        print("Failed to connect to the database")
        print(f"Error: {e}")
        time.sleep(2) """