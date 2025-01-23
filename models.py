from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Author(Base):
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    slug = Column(String(200), unique=True, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    author = relationship("Author", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    author = relationship("Author", back_populates="comments")
    post = relationship("Post", back_populates="comments")

# Create database engine
DATABASE_URL = "sqlite:///./blog.db"
engine = create_engine(DATABASE_URL)

# Create all tables
def create_tables():
    Base.metadata.create_all(engine)
