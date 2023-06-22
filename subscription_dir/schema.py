import graphene
from graphene_django import DjangoObjectType
from graphene import String, Int
from .models import Subscription


class SubscriptionType(DjangoObjectType):
    class Meta:
        model = Subscription
        fields = ["id", "userId", "regionId", "category", "urgency", "severity", "subscribeBy"]


# class CreateSubscription(graphene.Mutation):
#     class Arguments:
#         userId = Int(required=True)
#         regionId = Int(required=True)
#         category = String(required=True)
#         urgency = String(required=True)
#         severity = String(required=True)
#         subscribeBy = String(required=True)
#
#     region = graphene.Field(SubscriptionType)
#
#     def mutate(self, userId, regionId, category, urgency, severity, subscribeBy):
#         subscription = Subscription(userId=userId, regionId=regionId, category=category,
#                                     urgency=urgency, severity=severity, subscribeBy=subscribeBy)
#         subscription.save()
#         return CreateSubscription(subscription=subscription)
#
#
# class Mutation(graphene.ObjectType):
#     create_subscription = CreateSubscription.Field()


class Query(graphene.ObjectType):
    list_subscription = graphene.List(SubscriptionType)

    def resolve_list_subscription(root, info):
        # We can easily optimize query count in the resolve method
        return Subscription.objects.all()


# schema = graphene.Schema(query=Query, mutation=Mutation)
schema = graphene.Schema(query=Query)
