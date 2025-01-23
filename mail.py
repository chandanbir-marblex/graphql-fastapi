import asyncio

import graphene

# from graphene_file_upload.scalars import Upload

from starlette.applications import Starlette
from starlette_graphene3 import GraphQLApp, make_graphiql_handler


class User(graphene.ObjectType):
    id = graphene.ID()
    name = graphene.String()


class Query(graphene.ObjectType):
    me = graphene.Field(User)

    def resolve_me(root, info):
        return {"id": "john", "name": "John"}


# class Mutation(graphene.ObjectType):
#     upload_file = FileUploadMutation.Field()


class Subscription(graphene.ObjectType):
    count = graphene.Int(upto=graphene.Int())

    async def subscribe_count(root, info, upto=3):
        for i in range(upto):
            yield i
            await asyncio.sleep(1)


app = Starlette()
schema = graphene.Schema(query=Query, subscription=Subscription)

app.mount("/", GraphQLApp(schema, on_get=make_graphiql_handler()))  # Graphiql IDE

# app.mount("/", GraphQLApp(schema, on_get=make_playground_handler()))  # Playground IDE
# app.mount("/", GraphQLApp(schema)) # no IDE
