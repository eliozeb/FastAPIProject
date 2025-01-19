from typing import Optional
from fastapi import Body, Depends, FastAPI, HTTPException, Response, status
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db # After creating the database and its tables, we can remov from the import statement the Base class and the get_db function
from .routers import auth, post, user


# Create the database tables 
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

while True:
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
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "title of post 2", "content": "content of post 2", "id": 2},
            {"title": "favorite food", "content": "I like pitza" , "id": 3}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None

def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
    return None

# include the routers in the app instance of FastAPI 
app.include_router(post.router) # include the post router in the app instance of FastAPI 
app.include_router(user.router) # include the user router in the app instance of FastAPI 
app.include_router(auth.router) # include the auth router in the app instance of FastAPI

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return "welcome to my api"