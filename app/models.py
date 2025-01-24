from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String, Boolean, text
from .database import Base, engine
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "Posts"
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    title = Column(String, index=True)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)

    owner = relationship("User")

class User(Base):
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key=True, index=True, nullable=False)
    name = Column(String, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

    phone_number = Column(String)

class Vote(Base):
    __tablename__ = "Votes"
    user_id = Column(Integer, ForeignKey(
        "Users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "Posts.id", ondelete="CASCADE"), primary_key=True)