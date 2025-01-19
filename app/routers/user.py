

######################################..... User .....#################################################################
from sqlalchemy.orm import Session
from fastapi import Body, Depends, FastAPI, HTTPException, Response, status, APIRouter
from .. import schemas, utils, models
from app.database import get_db

router = APIRouter(
        prefix="/users",
        tags=['Users'],
        responses={307: {"description": "Temporary Redirect"}}
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = utils.hash(user.password)
        user_dict = user.dict()
        user_dict["password"] = hashed_password
        
        new_user = models.User(**user_dict)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating user: {str(e)}"
        )


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id {id} was not found")
    return user

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[schemas.User])
def get_users(db: Session = Depends(get_db)):
    try:
        users = db.query(models.User).all()
        return users
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving posts: {str(e)}"
        )