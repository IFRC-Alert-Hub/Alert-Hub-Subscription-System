import json
from django.test import TestCase
from django.utils import timezone
from .models import Subscription, Alert
from .cache import get_subscription_alerts
from .external_alert_models import CapFeedAdmin1, CapFeedCountry, CapFeedAlert, CapFeedAlertinfo
from .subscription_alert_mapping import map_alert_to_subscription
#Since Subscription System can only have read-access to Alert DB, the tables in external models
# need to be simulated on Subscription DB, otherwise the test data will not be inserted.
#This makes sure that we could mock exact data we want on these models and test the operations
# that manipulate them.

# pylint: disable=too-many-locals
class SubscriptionManagerTestCase(TestCase):
    # Setup data for the tests
    @classmethod
    def setUpClass(cls):
        teyvat_1 = CapFeedCountry.objects.create(name="Teyvat_1")
        teyvat_1.save()
        teyvat_2 = CapFeedCountry.objects.create(name="Teyvat_2")
        teyvat_2.save()

        # create admin data for migrations
        admin1_1 = CapFeedAdmin1.objects.create(name="Meng De", country=teyvat_1)
        admin1_1.save()
        admin1_2 = CapFeedAdmin1.objects.create(name="Li Yue", country=teyvat_1)
        admin1_2.save()
        admin1_3 = CapFeedAdmin1.objects.create(name="Xu Mi", country=teyvat_2)
        admin1_3.save()
        admin1_4 = CapFeedAdmin1.objects.create(name="Feng Dan", country=teyvat_2)
        admin1_4.save()

        #create alert data
        alert_1 = CapFeedAlert.objects.create(sent=timezone.now(), country=teyvat_1)
        alert_1.admin1s.add(admin1_1, admin1_2)
        alert_1.save()
        alert_info_1 = CapFeedAlertinfo.objects.create(category="Met",
                                                       event="Marine Weather Statement",
                                                       urgency="Expected",
                                                       severity="Minor",
                                                       certainty="Observed",
                                                       alert=alert_1)
        alert_info_2 = CapFeedAlertinfo.objects.create(category="Met",
                                                       event="Thunderstormwarning",
                                                       urgency="Future",
                                                       severity="Moderate",
                                                       certainty="Likely",
                                                       alert=alert_1)
        alert_info_1.save()
        alert_info_2.save()

        alert_2 = CapFeedAlert.objects.create(sent=timezone.now(), country=teyvat_2)
        alert_2.admin1s.add(admin1_3, admin1_4)
        alert_2.save()
        alert_info_3 = CapFeedAlertinfo.objects.create(category="Met",
                                                       event="Marine Weather Statement",
                                                       urgency="Expected",
                                                       severity="Minor",
                                                       certainty="Likely",
                                                       alert=alert_2)
        alert_info_4 = CapFeedAlertinfo.objects.create(category="Met",
                                                       event="Thunderstormwarning",
                                                       urgency="Immediate",
                                                       severity="Moderate",
                                                       certainty="Observed",
                                                       alert=alert_2)
        alert_info_3.save()
        alert_info_4.save()

        alert_3 = CapFeedAlert.objects.create(sent=timezone.now(), country=teyvat_1)
        alert_3.admin1s.add(admin1_1)
        alert_3.save()
        alert_info_5 = CapFeedAlertinfo.objects.create(category="Met",
                                                       event="Marine Weather Statement",
                                                       urgency="Expected",
                                                       severity="Minor",
                                                       certainty="Possible",
                                                       alert=alert_3)
        alert_info_5.save()

        alert_4 = CapFeedAlert.objects.create(sent=timezone.now(), country=teyvat_2)
        alert_4.admin1s.add(admin1_4)
        alert_4.save()
        alert_info_6 = CapFeedAlertinfo.objects.create(category="Met",
                                                       event="Marine Weather Statement",
                                                       urgency="Expected",
                                                       severity="Severe",
                                                       certainty="Possible",
                                                       alert=alert_4)
        alert_info_6.save()

        super(SubscriptionManagerTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        # Clean up any resources if necessary
        super().tearDownClass()

    # Test: Creation of subscriptions and check whether subscriptions matched expected list of
    # alerts
    def test_subscription_creation_1(self):
        urgency_list = ["Expected","Future"]
        severity_list = ["Minor", "Moderate"]
        certainty_list = ["Likely", "Observed", "Possible"]
        subscription = Subscription.objects.create(subscription_name="Subscription 1",
                                                   user_id=1,
                                                   country_ids=[1],
                                                   admin1_ids=[1,2],
                                                   urgency_array=urgency_list,
                                                   severity_array=severity_list,
                                                   certainty_array=certainty_list,
                                                   subscribe_by=[1],
                                                   sent_flag=0)
        expected = [1,3]
        actual = []
        for alert in subscription.alert_set.all():
            actual.append(alert.id)
        self.assertListEqual(expected,actual)

        #subscription.delete()

    def test_subscription_creation_2(self):
        urgency_list = ["Expected"]
        severity_list = ["Severe"]
        certainty_list = ["Possible"]
        subscription = Subscription.objects.create(subscription_name="Subscription 2",
                                                   user_id=1,
                                                   country_ids=[2],
                                                   admin1_ids=[3,4],
                                                   urgency_array=urgency_list,
                                                   severity_array=severity_list,
                                                   certainty_array=certainty_list,
                                                   subscribe_by=[1],
                                                   sent_flag=0)
        expected = [4]
        actual = []
        for alert in subscription.alert_set.all():
            actual.append(alert.id)
        self.assertListEqual(expected,actual)

        subscription.delete()


    def test_subscription_creation_all_alerts_in_country_1(self):
        urgency_list = ["Expected","Immediate","Future"]
        severity_list = ["Minor","Severe","Moderate"]
        certainty_list = ["Likely","Possible","Observed"]
        subscription = Subscription.objects.create(subscription_name="Subscription 3",
                                                   user_id=1,
                                                   country_ids=[2],
                                                   admin1_ids=[1,2],
                                                   urgency_array=urgency_list,
                                                   severity_array=severity_list,
                                                   certainty_array=certainty_list,
                                                   subscribe_by=[1],
                                                   sent_flag=0)
        expected = [1,3]
        actual = []
        for alert in subscription.alert_set.all():
            actual.append(alert.id)
        self.assertListEqual(expected, actual)

        subscription.delete()

    def test_subscription_creation_all_alerts_in_country_2(self):
        urgency_list = ["Expected", "Immediate", "Future"]
        severity_list = ["Minor", "Severe", "Moderate"]
        certainty_list = ["Likely", "Possible", "Observed"]
        subscription = Subscription.objects.create(subscription_name="Subscription 4",
                                                   user_id=1,
                                                   country_ids=[2],
                                                   admin1_ids=[3,4],
                                                   urgency_array=urgency_list,
                                                   severity_array=severity_list,
                                                   certainty_array=certainty_list,
                                                   subscribe_by=[1],
                                                   sent_flag=0)
        expected = [2, 4]
        actual = []
        for alert in subscription.alert_set.all():
            actual.append(alert.id)
        self.assertListEqual(expected, actual)

        subscription.delete()

    # Test: update subscription by severity, certainty, and urgency and check corresponding alerts
    def test_subscription_update_1(self):
        urgency_list = ["Expected", "Immediate", "Future"]
        severity_list = ["Minor", "Severe", "Moderate"]
        certainty_list = ["Likely", "Possible", "Observed"]
        subscription = Subscription.objects.create(subscription_name="Subscription 5",
                                                   user_id=1,
                                                   country_ids=[2],
                                                   admin1_ids=[3,4],
                                                   urgency_array=urgency_list,
                                                   severity_array=severity_list,
                                                   certainty_array=certainty_list,
                                                   subscribe_by=[1],
                                                   sent_flag=0)
        expected = [2,4]
        actual = []
        for alert in subscription.alert_set.all():
            actual.append(alert.id)
        self.assertListEqual(expected, actual)

        #Update urgency, severity, certainty for the subscription
        urgency_list = ["Expected"]
        severity_list = ["Severe"]
        certainty_list = ["Possible"]
        subscription.urgency_array = urgency_list
        subscription.severity_array = severity_list
        subscription.certainty_array = certainty_list

        subscription.save()

        expected = [4]
        actual = []
        for alert in subscription.alert_set.all():
            actual.append(alert.id)
        self.assertListEqual(expected,actual)

        subscription.delete()

        # Test: update subscription by regions and check corresponding alerts
    def test_subscription_update_2(self):
        urgency_list = ["Expected", "Immediate", "Future"]
        severity_list = ["Minor", "Severe", "Moderate"]
        certainty_list = ["Likely", "Possible", "Observed"]
        subscription = Subscription.objects.create(subscription_name="Subscription 6",
                                                    user_id=1,
                                                    country_ids=[2],
                                                    admin1_ids=[1, 2],
                                                    urgency_array=urgency_list,
                                                    severity_array=severity_list,
                                                    certainty_array=certainty_list,
                                                    subscribe_by=[1],
                                                    sent_flag=0)
        expected = [1, 3]
        actual = []
        for alert in subscription.alert_set.all():
            actual.append(alert.id)
        self.assertListEqual(expected, actual)

        # Update admin1 for the subscription
        admin1_ids=[3, 4]
        subscription.admin1_ids = admin1_ids
        subscription.save()

        expected = [2,4]
        actual = []
        for alert in subscription.alert_set.all():
            actual.append(alert.id)
        self.assertListEqual(expected, actual)

        subscription.delete()
    # Test: delete subscription and check many subscription - to - many field
    def test_subscription_delete_1(self):
        urgency_list = ["Expected", "Immediate", "Future"]
        severity_list = ["Minor", "Severe", "Moderate"]
        certainty_list = ["Likely", "Possible", "Observed"]
        subscription = Subscription.objects.create(subscription_name="Subscription 7",
                                                   user_id=1,
                                                   country_ids=[2],
                                                   admin1_ids=[1, 2],
                                                   urgency_array=urgency_list,
                                                   severity_array=severity_list,
                                                   certainty_array=certainty_list,
                                                   subscribe_by=[1],
                                                   sent_flag=0)
        expected = [1, 3]
        actual = []
        for alert in subscription.alert_set.all():
            actual.append(alert.id)
        self.assertListEqual(expected, actual)

        # Delete the subscription
        subscription.delete()

        #Check if there is still many-to-many relationship between deleted subscriptions and
        # corresponding alerts

        for alert_id in actual:
            alert = Alert.objects.filter(id = alert_id).first()
            alert_subscriptions = alert.subscriptions.all()
            self.assertQuerysetEqual(alert_subscriptions, [])


    def test_subscription_delete_2(self):
        urgency_list = ["Expected"]
        severity_list = ["Severe"]
        certainty_list = ["Possible"]
        subscription = Subscription.objects.create(subscription_name="Subscription 8",
                                                   user_id=1,
                                                   country_ids=[2],
                                                   admin1_ids=[3, 4],
                                                   urgency_array=urgency_list,
                                                   severity_array=severity_list,
                                                   certainty_array=certainty_list,
                                                   subscribe_by=[1],
                                                   sent_flag=0)
        expected = [4]
        actual = []
        for alert in subscription.alert_set.all():
            actual.append(alert.id)
        self.assertListEqual(expected, actual)

        subscription.delete()

        #Check if there is still many-to-many relationship between deleted subscriptions and
        # corresponding alerts
        for alert_id in actual:
            alert = Alert.objects.filter(id = alert_id).first()
            alert_subscriptions = alert.subscriptions.all()
            self.assertQuerysetEqual(alert_subscriptions, [])

    # Test: When a new subscription is created, test whether the cache that stores all alert
    # details of that subscription returns a list that matched list of expected alerts
    def test_subscription_creation_alerts_cache_1(self):
        urgency_list = ["Expected","Future"]
        severity_list = ["Minor", "Moderate"]
        certainty_list = ["Likely", "Observed", "Possible"]
        subscription = Subscription.objects.create(subscription_name="Subscription 9",
                                                   user_id=1,
                                                   country_ids=[1],
                                                   admin1_ids=[1,2],
                                                   urgency_array=urgency_list,
                                                   severity_array=severity_list,
                                                   certainty_array=certainty_list,
                                                   subscribe_by=[1],
                                                   sent_flag=0)
        #Get all subscription alerts details and put them into a list as expected value
        expected = [1, 3]
        expected_subscription_alerts_info = []
        for alert_id in expected:
            alert = Alert.objects.get(id=alert_id)
            expected_subscription_alerts_info.append(json.loads(alert.serialised_string))

        actual_subscription_alerts_info = json.loads(get_subscription_alerts(subscription.id))
        self.assertListEqual(expected_subscription_alerts_info,actual_subscription_alerts_info)

        subscription.delete()

    def test_subscription_creation_alerts_cache_2(self):
        urgency_list = ["Expected"]
        severity_list = ["Severe"]
        certainty_list = ["Possible"]
        subscription = Subscription.objects.create(subscription_name="Subscription 10",
                                                   user_id=1,
                                                   country_ids=[2],
                                                   admin1_ids=[3,4],
                                                   urgency_array=urgency_list,
                                                   severity_array=severity_list,
                                                   certainty_array=certainty_list,
                                                   subscribe_by=[1],
                                                   sent_flag=0)
        expected = [4]
        expected_subscription_alerts_info = []
        for alert_id in expected:
            alert = Alert.objects.get(id=alert_id)
            expected_subscription_alerts_info.append(json.loads(alert.serialised_string))

        actual_subscription_alerts_info = json.loads(get_subscription_alerts(subscription.id))
        self.assertListEqual(expected_subscription_alerts_info, actual_subscription_alerts_info)

        subscription.delete()


    def test_subscription_creation_alerts_cache_3(self):
        urgency_list = ["Expected","Immediate","Future"]
        severity_list = ["Minor","Severe","Moderate"]
        certainty_list = ["Likely","Possible","Observed"]
        subscription = Subscription.objects.create(subscription_name="Subscription 11",
                                                   user_id=1,
                                                   country_ids=[2],
                                                   admin1_ids=[1,2],
                                                   urgency_array=urgency_list,
                                                   severity_array=severity_list,
                                                   certainty_array=certainty_list,
                                                   subscribe_by=[1],
                                                   sent_flag=0)
        expected = [1,3]
        expected_subscription_alerts_info = []
        for alert_id in expected:
            alert = Alert.objects.get(id=alert_id)
            expected_subscription_alerts_info.append(json.loads(alert.serialised_string))

        actual_subscription_alerts_info = json.loads(get_subscription_alerts(subscription.id))
        self.assertListEqual(expected_subscription_alerts_info, actual_subscription_alerts_info)

        subscription.delete()

    def test_subscription_creation_alerts_cache_4(self):
        urgency_list = ["Expected", "Immediate", "Future"]
        severity_list = ["Minor", "Severe", "Moderate"]
        certainty_list = ["Likely", "Possible", "Observed"]
        subscription = Subscription.objects.create(subscription_name="Subscription 12",
                                                   user_id=1,
                                                   country_ids=[2],
                                                   admin1_ids=[3,4],
                                                   urgency_array=urgency_list,
                                                   severity_array=severity_list,
                                                   certainty_array=certainty_list,
                                                   subscribe_by=[1],
                                                   sent_flag=0)
        expected = [2, 4]
        expected_subscription_alerts_info = []
        for alert_id in expected:
            alert = Alert.objects.get(id=alert_id)
            expected_subscription_alerts_info.append(json.loads(alert.serialised_string))

        actual_subscription_alerts_info = json.loads(get_subscription_alerts(subscription.id))
        self.assertListEqual(expected_subscription_alerts_info, actual_subscription_alerts_info)

        subscription.delete()

    # Test: update subscription by severity, certainty, urgency, and check whether the cache stores
    # the list of alerts details that matched the updated subscription.
    def test_subscription_update_alerts_cache_1(self):
        urgency_list = ["Expected", "Immediate", "Future"]
        severity_list = ["Minor", "Severe", "Moderate"]
        certainty_list = ["Likely", "Possible", "Observed"]
        subscription = Subscription.objects.create(subscription_name="Subscription 13",
                                                   user_id=1,
                                                   country_ids=[2],
                                                   admin1_ids=[3,4],
                                                   urgency_array=urgency_list,
                                                   severity_array=severity_list,
                                                   certainty_array=certainty_list,
                                                   subscribe_by=[1],
                                                   sent_flag=0)

        #Update urgency, severity, certainty for the subscription
        urgency_list = ["Expected"]
        severity_list = ["Severe"]
        certainty_list = ["Possible"]
        subscription.urgency_array = urgency_list
        subscription.severity_array = severity_list
        subscription.certainty_array = certainty_list

        subscription.save()

        #Check the list of alerts that mapped updated subscription
        expected = [4]
        expected_subscription_alerts_info = []
        for alert_id in expected:
            alert = Alert.objects.get(id=alert_id)
            expected_subscription_alerts_info.append(json.loads(alert.serialised_string))

        actual_subscription_alerts_info = json.loads(get_subscription_alerts(subscription.id))
        self.assertListEqual(expected_subscription_alerts_info, actual_subscription_alerts_info)

        subscription.delete()

    # Test: update subscription by regions and check whether the cache stores the list of alerts
    # details that matched the updated subscription.
    def test_subscription_update_alerts_cache_2(self):
        urgency_list = ["Expected", "Immediate", "Future"]
        severity_list = ["Minor", "Severe", "Moderate"]
        certainty_list = ["Likely", "Possible", "Observed"]
        subscription = Subscription.objects.create(subscription_name="Subscription 14",
                                                    user_id=1,
                                                    country_ids=[2],
                                                    admin1_ids=[1, 2],
                                                    urgency_array=urgency_list,
                                                    severity_array=severity_list,
                                                    certainty_array=certainty_list,
                                                    subscribe_by=[1],
                                                    sent_flag=0)

        # Update admin1 for the subscription
        admin1_ids=[3, 4]
        subscription.admin1_ids = admin1_ids
        subscription.save()

        # Check the list of alerts that mapped updated subscription
        expected = [2,4]
        expected_subscription_alerts_info = []
        for alert_id in expected:
            alert = Alert.objects.get(id=alert_id)
            expected_subscription_alerts_info.append(json.loads(alert.serialised_string))

        actual_subscription_alerts_info = json.loads(get_subscription_alerts(subscription.id))
        self.assertListEqual(expected_subscription_alerts_info, actual_subscription_alerts_info)

        subscription.delete()

    # Test: Delete subscription and test if the cache has no record about the subscription
    def test_subscription_deletion_alerts_cache_1(self):
        urgency_list = ["Expected", "Immediate", "Future"]
        severity_list = ["Minor", "Severe", "Moderate"]
        certainty_list = ["Likely", "Possible", "Observed"]
        subscription = Subscription.objects.create(subscription_name="Subscription 15",
                                                   user_id=1,
                                                   country_ids=[2],
                                                   admin1_ids=[1, 2],
                                                   urgency_array=urgency_list,
                                                   severity_array=severity_list,
                                                   certainty_array=certainty_list,
                                                   subscribe_by=[1],
                                                   sent_flag=0)
        expected = [1, 3]
        actual = []
        for alert in subscription.alert_set.all():
            actual.append(alert.id)
        self.assertListEqual(expected, actual)

        # Delete the subscription
        subscription.delete()
        # Check if the cache does not have the record of subscription
        self.assertEqual(get_subscription_alerts(subscription.id), False)


    def test_subscription_deletion_alerts_cache_2(self):
        urgency_list = ["Expected"]
        severity_list = ["Severe"]
        certainty_list = ["Possible"]
        subscription = Subscription.objects.create(subscription_name="Subscription 16",
                                                   user_id=1,
                                                   country_ids=[2],
                                                   admin1_ids=[3, 4],
                                                   urgency_array=urgency_list,
                                                   severity_array=severity_list,
                                                   certainty_array=certainty_list,
                                                   subscribe_by=[1],
                                                   sent_flag=0)

        subscription.delete()
        # Check if the cache does not have the record of subscription
        self.assertEqual(get_subscription_alerts(subscription.id), False)

    # Test incoming alert that is not existed
    def test_incoming_alert_that_is_not_existed(self):
        result = map_alert_to_subscription(100)
        expected = "Alert with id 100 is not existed"
        self.assertEqual(expected, result)



    # Test incoming alert is already converted
    def test_incoming_alert_with_already_existed_id(self):
        #Create New subscription that maps the incoming alert
        urgency_list = ["Expected", "Future"]
        severity_list = ["Minor", "Moderate"]
        certainty_list = ["Likely", "Observed"]
        Subscription.objects.create(subscription_name="Common Subscription",
                                    user_id=1,
                                    country_ids=[2],
                                    admin1_ids=[1, 2],
                                    urgency_array=urgency_list,
                                    severity_array=severity_list,
                                    certainty_array=certainty_list,
                                    subscribe_by=[1],
                                    sent_flag=0)
        #Try to map alert with id 2 to the new subscription, though it is already mapped to the
        # above susbcription
        result = map_alert_to_subscription(1)
        expected = "Alert with id 1 is already converted and matched subscription"
        self.assertEqual(expected, result)

    # Test incoming alert and test if it matches the existing subscription
    def test_incoming_alert_with_non_existed_id_3(self):
        urgency_list = ["Expected", "Future"]
        severity_list = ["Minor", "Moderate"]
        certainty_list = ["Likely", "Observed"]
        common_subscription = Subscription.objects.create(subscription_name="Common Subscription",
                                                            user_id=1,
                                                            country_ids=[2],
                                                            admin1_ids=[1, 2],
                                                            urgency_array=urgency_list,
                                                            severity_array=severity_list,
                                                            certainty_array=certainty_list,
                                                            subscribe_by=[1],
                                                            sent_flag=0)

        # simulate
        teyvat_1 = CapFeedCountry.objects.get(id=1)
        admin1_1 = CapFeedAdmin1.objects.get(id=1)
        admin1_2 = CapFeedAdmin1.objects.get(id=2)
        mocked_incoming_alert = CapFeedAlert.objects.create(sent=timezone.now(), country=teyvat_1)
        mocked_incoming_alert.admin1s.add(admin1_1, admin1_2)
        mocked_incoming_alert.save()
        alert_info_1 = CapFeedAlertinfo.objects.create(category="Met",
                                                       event="Marine Weather Statement",
                                                       urgency="Expected",
                                                       severity="Minor",
                                                       certainty="Observed",
                                                       alert=mocked_incoming_alert)

        # Check if the cache does not have the record of subscription


    # Test add alert and test cache delete alert
    # Test add alert is not mapped with any susbcription

    # Test delete alert with id that is not existed
    # Test delete alert and test many subscription - to - many alerts
    # Test delete alert and test cache
    # Test delete alert that is not mapped with any subscription(rare case)

    # Test map all subscriptions
