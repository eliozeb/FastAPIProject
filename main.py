from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status
from pydantic import BaseModel

app = FastAPI()

# pydantic : a library fot Type of the model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True # an optional field to our schema
    rating: Optional[int] = None # an optional field to our schema

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "title of post 2", "content": "content of post 2", "id": 2},
            {"title": "favorite food", "content": "I like pitza" , "id": 3}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None

@app.get("/", status_code=status.HTTP_200_OK)
def root():
    return {"message": "welcome to my api"}

@app.get("/posts", status_code=status.HTTP_200_OK)
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict["id"] = len(my_posts) + 1
    my_posts.append( post_dict )
    return {"data": post_dict}

@app.get("/posts/latest", status_code=status.HTTP_200_OK)
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"data": post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    print(id)
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"data: {post}, message: Post with id {id} was not found")
    return {"data": post, "message": f"This is the post you requested {id}"}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    post = find_post(id) # find the post
    if not post: # if post not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} was not found")
    my_posts.remove(post) # remove the post
    return Response(status_code=status.HTTP_204_NO_CONTENT) # return a message
