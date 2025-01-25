from fastapi import FastAPI, status
from . import models
from .database import engine  # After creating the database and its tables, we can remov from the import statement the Base class and the get_db function
from .routers import auth, post, user, vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

print(settings.database_username)

# Create the database tables 
#models.Base.metadata.create_all(bind=engine) 


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware, # 
    allow_origins=origins, #
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

# The following code is for demonstration purposes only 
""" my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "title of post 2", "content": "content of post 2", "id": 2},
            {"title": "favorite food", "content": "I like pitza" , "id": 3}]

# The following code is for demonstration purposes only 
def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None

    
# The following code is for demonstration purposes only
def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
    return None """

# include the routers in the app instance of FastAPI 
app.include_router(post.router) # include the post router in the app instance of FastAPI 
app.include_router(user.router) # include the user router in the app instance of FastAPI 
app.include_router(auth.router) # include the auth router in the app instance of FastAPI
app.include_router(vote.router) # include the vote router in the app instance of FastAPI


@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {
        "message": "Welcome to FastAPI Project",
        "documentation": "/docs",
        "github": "https://github.com/eliozeb/FastAPIProject"
    }