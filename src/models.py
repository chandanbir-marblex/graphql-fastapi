from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime as dt
from typing import List
from graphene_sqlalchemy import SQLAlchemyObjectType


class Base(DeclarativeBase):
    created_at: Mapped[dt] = mapped_column(default=dt.now())
    updated_at: Mapped[dt] = mapped_column(default=dt.now(), onupdate=dt.now())


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    name: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)


class UserType(SQLAlchemyObjectType):
    class Meta:
        model = User


class Blog(Base):
    __tablename__ = "blogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    body: Mapped[str] = mapped_column(nullable=False)
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )


class BlogType(SQLAlchemyObjectType):
    class Meta:
        model = Blog
