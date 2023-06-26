import graphene
from graphene_django import DjangoObjectType
from .models import Subscription


class SubscriptionType(DjangoObjectType):
    class Meta:
        model = Subscription
        fields = ["id", "user_id", "country_ids", "urgency_array", "severity_array",
                  "certainty_array", "subscribe_by"]


class CreateSubscription(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        country_ids = graphene.List(graphene.Int)
        urgency_array = graphene.List(graphene.String)
        severity_array = graphene.List(graphene.String)
        certainty_array = graphene.List(graphene.String)
        subscribe_by = graphene.List(graphene.String)

    subscription = graphene.Field(SubscriptionType)

    def mutate(self, info, user_id, country_ids, urgency_array, severity_array, certainty_array,
               subscribe_by):
        subscription = Subscription(user_id=user_id,
                                    country_ids=country_ids,
                                    urgency_array=urgency_array,
                                    severity_array=severity_array,
                                    certainty_array=certainty_array,
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
        urgency_array = graphene.List(graphene.String)
        severity_array = graphene.List(graphene.String)
        certainty_array = graphene.List(graphene.String)
        subscribe_by = graphene.List(graphene.String)

    subscription = graphene.Field(SubscriptionType)

    def mutate(self, info, subscription_id, user_id, country_ids, urgency_array, severity_array,
               certainty_array, subscribe_by):
        subscription = Subscription.objects.get(id=subscription_id)
        subscription.user_id = user_id
        subscription.country_ids = country_ids
        subscription.urgency_array = urgency_array
        subscription.severity_array = severity_array
        subscription.certainty_array = certainty_array
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
                                      urgency_array=graphene.List(graphene.String),
                                      severity_array=graphene.List(graphene.String),
                                      certainty_array=graphene.List(graphene.String))
    get_subscription = graphene.Field(SubscriptionType,
                                      subscription_id=graphene.Int())

    def resolve_list_all_subscription(self, info):
        return Subscription.objects.all()

    def resolve_list_subscription_by_user_id(self, info, user_id):
        return Subscription.objects.filter(user_id=user_id)

    def resolve_list_subscription(self, info, country_ids, urgency_array, severity_array,
                                  certainty_array):
        return Subscription.objects.filter(country_ids__contains=country_ids,
                                           urgency_array__contains=urgency_array,
                                           severity_array__contains=severity_array,
                                           certainty_array__contains=certainty_array)

    def resolve_get_subscription(self, info, subscription_id):
        return Subscription.objects.get(id=subscription_id)


schema = graphene.Schema(query=Query, mutation=Mutation)
