import graphene
from graphene_django import DjangoObjectType
from .models import User, Region, Subscription


class UserType(DjangoObjectType):
    class Meta:
        model = User
        field = ("id", "email", "whatsapp")


class RegionType(DjangoObjectType):
    class Meta:
        model = Region
        field = ("id", "name", "polygon")


class SubscriptionType(DjangoObjectType):
    class Meta:
        model = Subscription
        fields = ["id", "user", "region", "category", "urgency", "severity", "subscribe_by"]


class CreateSubscription(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        region_id = graphene.Int(required=True)
        category = graphene.String(required=True)
        urgency = graphene.Int(required=True)
        severity = graphene.Int(required=True)
        subscribe_by = graphene.String(required=True)

    subscription = graphene.Field(SubscriptionType)

    def mutate(self, info, user_id, region_id, category, urgency, severity, subscribe_by):
        user_object = User.objects.get(id=user_id)
        region_object = Region.objects.get(id=region_id)
        subscription = Subscription(user=user_object,
                                    region=region_object,
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
        region_id = graphene.Int(required=True)
        category = graphene.String(required=True)
        urgency = graphene.Int(required=True)
        severity = graphene.Int(required=True)
        subscribe_by = graphene.String(required=True)

    subscription = graphene.Field(SubscriptionType)

    def mutate(self, info,
               subscription_id, user_id, region_id, category, urgency, severity, subscribe_by):
        subscription = Subscription.objects.get(id=subscription_id)
        subscription.user = User.objects.get(id=user_id)
        subscription.region = Region.objects.get(id=region_id)
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
    list_subscription = graphene.List(SubscriptionType,
                                      region_id=graphene.Int(default_value=-1),
                                      category=graphene.String(),
                                      urgency=graphene.Int(),
                                      severity=graphene.Int())
    get_subscription = graphene.Field(SubscriptionType,
                                      subscription_id=graphene.Int())

    def resolve_list_all_subscription(self, info):
        return Subscription.objects.all()

    def resolve_list_subscription(self, info, region_id, category, urgency, severity):
        if region_id == -1:
            return Subscription.objects.filter(category=category,
                                               urgency__gte=urgency,
                                               severity__gte=severity)
        return Subscription.objects.filter(region_id=region_id,
                                           category=category,
                                           urgency__gte=urgency,
                                           severity__gte=severity)


    def resolve_get_subscription(self, info, subscription_id):
        return Subscription.objects.get(id=subscription_id)


schema = graphene.Schema(query=Query, mutation=Mutation)
