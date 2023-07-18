import graphene
from graphene_django import DjangoObjectType
from .models import Polygon


class PolygonType(DjangoObjectType):
    class Meta:
        model = Polygon
        fields = ["id", "user_id", "vertices"]


# class Mutation(graphene.ObjectType):
#     create_polygon = CreatePolygon.Field()


class Query(graphene.ObjectType):
    list_polygon = graphene.List(PolygonType)

    def resolve_list_polygon(self, info):
        return Polygon.objects.all()


schema = graphene.Schema(query=Query)
# schema = graphene.Schema(query=Query, mutation=Mutation)
