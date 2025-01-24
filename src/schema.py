import graphene
from .query import BlogQuery
from .mutation import BlogMutation
from .subscription import BlogSubscription


class Query(BlogQuery):
    pass


class Mutation(BlogMutation):
    pass


class Subscription(BlogSubscription):
    pass


# schema = graphene.Schema(query=Query, mutation=Mutation, )
schema = graphene.Schema(query=Query, subscription=Subscription)
