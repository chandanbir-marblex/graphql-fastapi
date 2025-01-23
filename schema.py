import graphene
from graphene import relay
from datetime import datetime
from typing import Optional
from slugify import slugify

from models import Author as AuthorModel
from models import Post as PostModel
from models import Comment as CommentModel
from database import database

class Author(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    email = graphene.String()
    bio = graphene.String()
    created_at = graphene.DateTime()
    posts = graphene.List(lambda: Post)
    comments = graphene.List(lambda: Comment)

class Post(graphene.ObjectType):
    id = graphene.Int()
    title = graphene.String()
    content = graphene.String()
    slug = graphene.String()
    author = graphene.Field(Author)
    created_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    comments = graphene.List(lambda: Comment)

class Comment(graphene.ObjectType):
    id = graphene.Int()
    content = graphene.String()
    author = graphene.Field(Author)
    post = graphene.Field(Post)
    created_at = graphene.DateTime()

class Query(graphene.ObjectType):
    posts = graphene.List(
        Post,
        limit=graphene.Int(default_value=10),
        offset=graphene.Int(default_value=0)
    )
    post = graphene.Field(Post, slug=graphene.String())
    authors = graphene.List(Author)
    author = graphene.Field(Author, id=graphene.Int())

    async def resolve_posts(self, info, limit=10, offset=0):
        query = "SELECT * FROM posts ORDER BY created_at DESC LIMIT :limit OFFSET :offset"
        return await database.fetch_all(query=query, values={"limit": limit, "offset": offset})

    async def resolve_post(self, info, slug):
        query = "SELECT * FROM posts WHERE slug = :slug"
        return await database.fetch_one(query=query, values={"slug": slug})

    async def resolve_authors(self, info):
        query = "SELECT * FROM authors"
        return await database.fetch_all(query=query)

    async def resolve_author(self, info, id):
        query = "SELECT * FROM authors WHERE id = :id"
        return await database.fetch_one(query=query, values={"id": id})

class CreateAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        bio = graphene.String()

    ok = graphene.Boolean()
    author = graphene.Field(lambda: Author)

    async def mutate(root, info, name: str, email: str, bio: Optional[str] = None):
        query = """
        INSERT INTO authors (name, email, bio, created_at)
        VALUES (:name, :email, :bio, :created_at)
        RETURNING *
        """
        values = {
            "name": name,
            "email": email,
            "bio": bio,
            "created_at": datetime.utcnow()
        }
        author = await database.fetch_one(query=query, values=values)
        return CreateAuthor(author=author, ok=True)

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)
        author_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    post = graphene.Field(lambda: Post)

    async def mutate(root, info, title: str, content: str, author_id: int):
        slug = slugify(title)
        query = """
        INSERT INTO posts (title, content, slug, author_id, created_at, updated_at)
        VALUES (:title, :content, :slug, :author_id, :created_at, :updated_at)
        RETURNING *
        """
        values = {
            "title": title,
            "content": content,
            "slug": slug,
            "author_id": author_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        post = await database.fetch_one(query=query, values=values)
        return CreatePost(post=post, ok=True)

class CreateComment(graphene.Mutation):
    class Arguments:
        content = graphene.String(required=True)
        post_id = graphene.Int(required=True)
        author_id = graphene.Int(required=True)

    ok = graphene.Boolean()
    comment = graphene.Field(lambda: Comment)

    async def mutate(root, info, content: str, post_id: int, author_id: int):
        query = """
        INSERT INTO comments (content, post_id, author_id, created_at)
        VALUES (:content, :post_id, :author_id, :created_at)
        RETURNING *
        """
        values = {
            "content": content,
            "post_id": post_id,
            "author_id": author_id,
            "created_at": datetime.utcnow()
        }
        comment = await database.fetch_one(query=query, values=values)
        return CreateComment(comment=comment, ok=True)

class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
    create_post = CreatePost.Field()
    create_comment = CreateComment.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
