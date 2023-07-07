from django.urls import path
from graphene_django.views import GraphQLView
from graphql_jwt.decorators import jwt_cookie
from user_dir.schema import schema

urlpatterns = [
    path('graphql', jwt_cookie(GraphQLView.as_view(graphiql=True, schema=schema))),
]
