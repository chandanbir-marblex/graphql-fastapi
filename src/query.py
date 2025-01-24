import graphene
from .models import BlogType, Blog
from .database import get_db
from fastapi import Depends
from sqlalchemy.orm import Session


class BlogQuery(graphene.ObjectType):
    all_blog = graphene.List(BlogType)
    blog_by_id = graphene.Field(BlogType, id=graphene.Int(required=True))

    def resolve_all_blog(root, info):
        db = next(get_db())
        try:
            result = db.query(Blog).all()
            print(result)
            return result
        finally:
            db.close()

    def resolve_blog_by_id(root, info, id):
        db = next(get_db())
        try:
            result = db.query(Blog).get(id)
            return result
        finally:
            db.close()
