import graphene
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required
from .models import Subscription


class SubscriptionType(DjangoObjectType):
    class Meta:
        model = Subscription
        fields = ["id", "subscription_name", "user_id", "country_ids", "district_ids",
                  "urgency_array", "severity_array", "certainty_array", "subscribe_by", "sent_flag"]


def create_subscription(user_id, subscription_name, country_ids, district_ids,
                        urgency_array, severity_array, certainty_array, subscribe_by, sent_flag):
    subscription = Subscription(user_id=user_id,
                                subscription_name=subscription_name,
                                country_ids=country_ids,
                                district_ids=district_ids,
                                urgency_array=urgency_array,
                                severity_array=severity_array,
                                certainty_array=certainty_array,
                                subscribe_by=subscribe_by,
                                sent_flag=sent_flag)
    subscription.save()
    return subscription


class CreateSubscription(graphene.Mutation):
    class Arguments:
        subscription_name = graphene.String(required=True)
        country_ids = graphene.List(graphene.Int)
        district_ids = graphene.List(graphene.Int)
        urgency_array = graphene.List(graphene.String)
        severity_array = graphene.List(graphene.String)
        certainty_array = graphene.List(graphene.String)
        subscribe_by = graphene.List(graphene.String)
        sent_flag = graphene.Int(required=True)

    subscription = graphene.Field(SubscriptionType)

    @login_required
    def mutate(self, info, subscription_name, country_ids, district_ids,
               urgency_array, severity_array, certainty_array, subscribe_by, sent_flag):
        subscription = create_subscription(info.context.user.id,
                                           subscription_name,
                                           country_ids,
                                           district_ids,
                                           urgency_array,
                                           severity_array,
                                           certainty_array,
                                           subscribe_by,
                                           sent_flag)
        return CreateSubscription(subscription=subscription)


class DeleteSubscription(graphene.Mutation):

    class Arguments:
        subscription_id = graphene.Int(required=True)

    success = graphene.Boolean()
    error_message = graphene.String()

    @login_required
    def mutate(self, info, subscription_id):
        subscription = Subscription.objects.get(id=subscription_id)
        login_user_id = info.context.user.id
        if subscription.user_id != login_user_id:
            return DeleteSubscription(success=False,
                                      error_message='Delete operation is not authorized '
                                                    'to this user.')
        subscription.delete()
        return DeleteSubscription(success=True)


class UpdateSubscription(graphene.Mutation):
    class Arguments:
        subscription_id = graphene.Int(required=True)
        subscription_name = graphene.String(required=True)
        country_ids = graphene.List(graphene.Int)
        district_ids = graphene.List(graphene.Int)
        urgency_array = graphene.List(graphene.String)
        severity_array = graphene.List(graphene.String)
        certainty_array = graphene.List(graphene.String)
        subscribe_by = graphene.List(graphene.String)
        sent_flag = graphene.Int(required=True)

    success = graphene.Boolean()
    error_message = graphene.String()

    def mutate(self, info, subscription_id, subscription_name,
               country_ids, district_ids,
               urgency_array, severity_array, certainty_array, subscribe_by, sent_flag):
        subscription = Subscription.objects.get(id=subscription_id)
        login_user_id = info.context.user.id
        if subscription.user_id != login_user_id:
            return UpdateSubscription(success=False,
                                      error_message='Update operation is not authorized '
                                                    'to this user.')
        subscription.subscription_name = subscription_name
        subscription.country_ids = country_ids
        subscription.district_ids = district_ids
        subscription.urgency_array = urgency_array
        subscription.severity_array = severity_array
        subscription.certainty_array = certainty_array
        subscription.subscribe_by = subscribe_by
        subscription.sent_flag = sent_flag
        subscription.save()
        return UpdateSubscription(success=True)


class Mutation(graphene.ObjectType):
    create_subscription = CreateSubscription.Field()
    delete_subscription = DeleteSubscription.Field()
    update_subscription = UpdateSubscription.Field()


class Query(graphene.ObjectType):
    list_all_subscription = graphene.List(SubscriptionType)
    list_subscription = graphene.List(SubscriptionType,
                                      country_ids=graphene.List(graphene.Int),
                                      district_ids=graphene.List(graphene.Int),
                                      urgency_array=graphene.List(graphene.String),
                                      severity_array=graphene.List(graphene.String),
                                      certainty_array=graphene.List(graphene.String))
    get_subscription = graphene.Field(SubscriptionType,
                                      subscription_id=graphene.Int())

    @login_required
    def resolve_list_all_subscription(self, info):
        return Subscription.objects.filter(user_id=info.context.user.id).order_by('-id')


    def resolve_list_subscription(self, info, country_ids, district_ids,
                                  urgency_array, severity_array, certainty_array):
        return Subscription.objects.filter(country_ids__contains=country_ids,
                                           district_ids__contains=district_ids,
                                           urgency_array__contains=urgency_array,
                                           severity_array__contains=severity_array,
                                           certainty_array__contains=certainty_array)\
            .order_by('-id')


    def resolve_get_subscription(self, info, subscription_id):
        return Subscription.objects.get(id=subscription_id)


schema = graphene.Schema(query=Query, mutation=Mutation)
