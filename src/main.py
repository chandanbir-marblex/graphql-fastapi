from fastapi import FastAPI
from .schema import schema
from starlette_graphene3 import GraphQLApp, make_graphiql_handler


app = FastAPI()


app.mount("/", GraphQLApp(schema, on_get=make_graphiql_handler()))
