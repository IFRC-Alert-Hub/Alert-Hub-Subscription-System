#Test Specification
#unit test
#Test comparation between alert and subscription


#Test add subscription and check many subscription - to - many alerts
#Test change subscription and check many subscription - to - many alerts
#Test delete subscription and check many subscription - to - many field

#Test add subscription and test cache
#Test change subscription and test cache
#Test delete subscription and test cache

#Test add alert and test many subscription - to - many alerts
#Test add alert and test cache delete alert and test many subscriptions to many alerts
#Test delete alert and test cache

#Test when alert is not mapped
#Test alert to be deleted is not existed test



import json
from unittest.mock import patch

from graphene_django.utils.testing import GraphQLTestCase
from django.test import Client
from django.contrib.auth import get_user_model
from django.test import TestCase
from .models import Subscription
from .external_alert_models import CapFeedAdmin1, CapFeedCountry

#Since Subscription System can only have read-access to Alert DB, the tables in external models
# will be simulated on Subscription DB. This makes sure that we could mock exact data we want and
# test their operations.
class SubscriptionManagerTestCase(TestCase):

    # Setup data for the tests
    def setUp(self):
        america = CapFeedCountry.objects.create(name="United States of America")
        america.save()
        # create data for migrations
        admin1 = CapFeedAdmin1.objects.create(name="America Shang Di Ya Gou", country=america)

    def test_model_creation(self):
        test_item = CapFeedCountry.objects.get(name="United States of America")