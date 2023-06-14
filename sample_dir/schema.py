import graphene
from graphene_django import DjangoObjectType
from .models import alert


class AlertInformation(DjangoObjectType):
    class Meta:
        model = alert
        fields = ( "name", "creation_date")

class Query(graphene.ObjectType):
    all_alerts = graphene.List(AlertInformation)
    def resolve_all_alerts(root, info):
        return alert.objects.all()
schema = graphene.Schema(query=Query)