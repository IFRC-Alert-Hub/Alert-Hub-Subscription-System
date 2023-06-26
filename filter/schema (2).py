import graphene
from graphene_django import DjangoObjectType
from graphene import String, Int
from .models import Alert, AlertInfo, Country, Region
import datetime
import requests
import secrets
from .views import compare_polygon
from django.db.models import Q



class RegionType(DjangoObjectType):
    class Meta:
        model = Region
        fields = ["id", "name", "polygon"]

class CountryType(DjangoObjectType):
    class Meta:
        model = Country
        fields = ["region_id", "id", "name", "society_name", "polygon", "centroid"]



class CreateRegion(graphene.Mutation):
    class Arguments:
        id = Int(required=True)
        name = String(required=True)
        polygon = String(required = True)

    region = graphene.Field(RegionType)

    def mutate(self, info, id, name, polygon):
        region = Region(id=id, name=name, polygon = polygon)
        region.save()
        return CreateRegion(region=region)

class CreateCountry(graphene.Mutation):
    class Arguments:
        id = Int(required=True)
        region_id = Int()
        name = String(required=True)
        society_name = String(required=True)
        polygon = String(required = True)
        centroid = String(required = True)

    country = graphene.Field(CountryType)

    def mutate(self, info, id, name, society_name, polygon, centroid, region_id=None):
        if region_id:
            country = Country(id=id, name=name, society_name= society_name, region_id=Region.objects.get(id=region_id), polygon = polygon, centroid=centroid)
        else:
            country = Country(id=id, name=name, society_name=society_name, region_id=None,
                              polygon=polygon, centroid=centroid)
        country.save()
        return CreateCountry(country=country)

class Mutation(graphene.ObjectType):
    create_region = CreateRegion.Field()
    create_country = CreateCountry.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
