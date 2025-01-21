######################################..... Post .....#################################################################
from sqlalchemy.orm import Session
from fastapi import Body, Depends, FastAPI, HTTPException, Response, status, APIRouter
from typing import List, Optional
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
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = None):
    try:
        posts = db.query(models.Post).order_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        """ .filter(models.Post.owner_id == current_user.id) """ # filter the posts that belong to the current user, but on social media we need to allow the user to see all the posts even if they do not belong to him 
        
        if not posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                                detail=f"Posts were not found")
        
        # its a social media, so we need to allow the user to see all the posts even if they do not belong to him 
        #if posts.first().owner_id != current_user.id:
        #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
        #                    detail="You are not allowed to perform requested action") # if the post does not belong to the current user 
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving posts: {str(e)}"
        )
    
    return posts   # return the posts that belong to the current user 

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    try:
        new_post = models.Post(owner_id=current_user.id, **post.dict())
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
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"data: {post}, message: Post with id {id} was not found")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first(): # if post not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You are not allowed to perform requested action") # if the post does not belong to the current user 
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT) # return a message

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_to_update = db.query(models.Post).filter(models.Post.id == id)
    
    if not post_to_update.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found")
    if post_to_update.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="You are not allowed to perform requested action") # if the post does not belong to the current user 
    
    post_to_update.update(post.dict(), synchronize_session=False)
    db.commit()
    
    return post_to_update.first()