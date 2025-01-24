import graphene
from sqlalchemy.engine import result


class CreateBlog(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        text = graphene.String()

    ok = graphene.Boolean()
    blog = graphene.Field(BlogType)

    def mutate(root, info, title, text):
        db = next(get_db())
        try:
            newblog = Blog(title=title, text=text, author=info.context.user)
            db.add(newblog)
            db.commit()
        finally:
            db.close()

        return CreateBlog(ok=True, blog=newblog)


class DeleteBlog(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    def mutate(root, info, id):
        try:
            db = next(get_db())
            existing_blog = db.query(Blog).get(id)
            if info.context.user == existing_blog.author:
                existing_blog.delete()
                return DeleteBlog(
                    ok=True,
                )
            return DeleteBlog(
                ok=False,
            )

        finally:
            db.close()


class UpdateBlog(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        text = graphene.String()

    ok = graphene.Boolean()
    blog = graphene.Field(BlogType)

    def mutate(root, info, id, title, text):

        try:
            db = next(get_db())
            existing_blog = db.query(Blog).get(id)
            if not existing_blog:
                return UpdateBlog(ok=False)
            if info.context.user == existing_blog.author:
                existing_blog.title = title
                existing_blog.text = text
                existing_blog.save()
                return UpdateBlog(ok=True, blog=existing_blog)
        except:
            return UpdateBlog(ok=False)
        finally:
            db.close()


class BlogMutation(graphene.ObjectType):
    create_blog = CreateBlog.Field()
    updateBlog = UpdateBlog.Field()
    delete_blog = DeleteBlog.Field()
