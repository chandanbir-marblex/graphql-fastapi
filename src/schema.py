import graphene
from .Query.blog_query import BlogQuery
from .Mutation.blog_mutation import BlogMutation
from .Subcription.blog_subscription import BlogSubscription


class Query(BlogQuery):
    pass


class Mutation(BlogMutation):
    pass


class Subscription(BlogSubscription):
    pass


# schema = graphene.Schema(query=Query, mutation=Mutation, )
schema = graphene.Schema(query=Query, mutation=Mutation, subscription=Subscription)
