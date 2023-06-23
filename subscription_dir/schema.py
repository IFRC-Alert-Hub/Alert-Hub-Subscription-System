import graphene
from graphene_django import DjangoObjectType
from .models import Subscription


class SubscriptionType(DjangoObjectType):
    class Meta:
        model = Subscription
        fields = ["id", "user_id", "country_ids", "category", "urgency", "severity", "subscribe_by"]


class CreateSubscription(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        country_ids = graphene.List(graphene.Int)
        category = graphene.String(required=True)
        urgency = graphene.Int(required=True)
        severity = graphene.Int(required=True)
        subscribe_by = graphene.String(required=True)

    subscription = graphene.Field(SubscriptionType)

    def mutate(self, info, user_id, country_ids, category, urgency, severity, subscribe_by):
        subscription = Subscription(user_id=user_id,
                                    country_ids=country_ids,
                                    category=category,
                                    urgency=urgency,
                                    severity=severity,
                                    subscribe_by=subscribe_by)
        subscription.save()
        return CreateSubscription(subscription=subscription)


class DeleteSubscription(graphene.Mutation):
    class Arguments:
        subscription_id = graphene.Int(required=True)

    subscription = graphene.Field(SubscriptionType)

    def mutate(self, info, subscription_id):
        subscription = Subscription.objects.get(id=subscription_id)
        subscription.delete()


class UpdateSubscription(graphene.Mutation):
    class Arguments:
        subscription_id = graphene.Int(required=True)
        user_id = graphene.Int(required=True)
        country_ids = graphene.List(graphene.Int)
        category = graphene.String(required=True)
        urgency = graphene.Int(required=True)
        severity = graphene.Int(required=True)
        subscribe_by = graphene.String(required=True)

    subscription = graphene.Field(SubscriptionType)

    def mutate(self, info,
               subscription_id, user_id, country_ids, category, urgency, severity, subscribe_by):
        subscription = Subscription.objects.get(id=subscription_id)
        subscription.user_id = user_id
        subscription.country_ids = country_ids
        subscription.category = category
        subscription.urgency = urgency
        subscription.severity = severity
        subscription.subscribe_by = subscribe_by
        subscription.save()
        return UpdateSubscription(subscription=subscription)


class Mutation(graphene.ObjectType):
    create_subscription = CreateSubscription.Field()
    delete_subscription = DeleteSubscription.Field()
    update_subscription = UpdateSubscription.Field()


class Query(graphene.ObjectType):
    list_all_subscription = graphene.List(SubscriptionType)
    list_subscription_by_user_id = graphene.List(SubscriptionType,
                                                 user_id=graphene.Int())
    list_subscription = graphene.List(SubscriptionType,
                                      country_ids=graphene.List(graphene.Int),
                                      category=graphene.String(),
                                      urgency=graphene.Int(),
                                      severity=graphene.Int())
    get_subscription = graphene.Field(SubscriptionType,
                                      subscription_id=graphene.Int())

    def resolve_list_all_subscription(self, info):
        return Subscription.objects.all()

    def resolve_list_subscription_by_user_id(self, info, user_id):
        return Subscription.objects.filter(user_id=user_id)

    def resolve_list_subscription(self, info, country_ids, category, urgency, severity):
        query_set = Subscription.objects.filter(urgency__gte=urgency,
                                               severity__gte=severity)
        if len(country_ids) > 0:
            query_set = query_set.filter(country_ids__contains=country_ids)

        if category != "":
            query_set = query_set.filter(category=category)

        return query_set

    def resolve_get_subscription(self, info, subscription_id):
        return Subscription.objects.get(id=subscription_id)


schema = graphene.Schema(query=Query, mutation=Mutation)
