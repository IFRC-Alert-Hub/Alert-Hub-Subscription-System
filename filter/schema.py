import graphene
from graphene_django import DjangoObjectType
from .models import Alert


class AlertInformation(DjangoObjectType):
    class Meta:
        model = Alert
        fields = ( "name", "creation_date")

class Query(graphene.ObjectType):
    all_alerts = graphene.List(AlertInformation)
    def resolve_all_alerts(self):
        return Alert.objects.all()
schema = graphene.Schema(query=Query)
