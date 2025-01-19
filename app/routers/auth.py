from urllib import response
from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database, oauth2, schemas, models, utils

router = APIRouter(
    prefix="/login",
    tags=['Authentication'],
    responses={307: {"description": "Temporary Redirect"}}
)


@router.post("/", status_code=status.HTTP_200_OK)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(database.get_db), response: Response = None):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    access_token = oauth2.create_access_token(data={"user_id": user.id})
        # Set cookie if needed
    if response:
        response.set_cookie(
            key="session", 
            value="session-value",
            httponly=True
        )
    return {"access_token": access_token, "token_type": "bearer"}

