######################################..... Post .....#################################################################
from sqlalchemy.orm import Session
from fastapi import Body, Depends, FastAPI, HTTPException, Response, status, APIRouter
from typing import List
from .. import oauth2, schemas, models
from app.database import get_db


router = APIRouter(
            prefix="/posts",
            tags=['Posts'],
            responses={307: {"description": "Temporary Redirect"}}
)


my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, 
            {"title": "title of post 2", "content": "content of post 2", "id": 2},
            {"title": "favorite food", "content": "I like pitza" , "id": 3}]
  


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    try:
        posts = db.query(models.Post).all()
        return posts
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving posts: {str(e)}"
        )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), get_current_user: int = Depends(oauth2.get_current_user)):
    try:
        new_post = models.Post(**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
        return  new_post
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating post: {str(e)}"
        )
    
@router.get("/latest", status_code=status.HTTP_200_OK)
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return post

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"data: {post}, message: Post with id {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first(): # if post not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) # return a message

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    post_to_update = db.query(models.Post).filter(models.Post.id == id)
    
    if not post_to_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    
    post_to_update.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return post_to_update.first()