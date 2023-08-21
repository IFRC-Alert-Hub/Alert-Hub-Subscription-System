import csv
import os
import django
from django.utils import timezone

os.environ["Test_Environment"] = 'True'

if 'WEBSITE_HOSTNAME' in os.environ:
    settings_module = "project.production"
else:
    settings_module = "project.settings"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

# Configure Django settings
django.setup()

from django.core.management import call_command, execute_from_command_line
from faker import Faker

from django.contrib.auth import get_user_model
from subscription_dir.models import Subscription
from subscription_manager_dir.external_alert_models import CapFeedCountry, CapFeedAdmin1, \
    CapFeedAlert, CapFeedAlertinfo

fake = Faker()
User = get_user_model()


def create_user(email, password):
    user = User.objects.create(
        email=email,
    )
    user.set_password(password)
    user.save()
    return user

def create_subscription(user):
    fake = Faker()
    return Subscription.objects.create(
        subscription_name=fake.sentence()[:-1],
        user_id=user.id,
        country_ids=[1],
        admin1_ids=[1],
        urgency_array=["Immediate"],
        severity_array=["Severe"],
        certainty_array=["Likely"],
        subscribe_by=["Email"],
        sent_flag=0,
    )

def generate_fake_users_and_subscriptions(count, csv_filename, num_subscriptions_per_user):
    fake = Faker()
    users = []

    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['email', 'password', 'subscription_ids']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(count):
            print("Creating users: {}/{}".format(i + 1, count))
            email = fake.email()
            password = fake.password()

            user = create_user(email, password)
            users.append(user)

            subscriptions = []
            for _ in range(num_subscriptions_per_user):
                subscription = create_subscription(user)
                subscriptions.append(subscription.id)

            writer.writerow({'email': email, 'password': password, 'subscription_ids': subscriptions})

    return users

def generate_simulated_alert(num_countries, num_admin1s_per_country, num_alerts_per_admin1):
    print("Creating alerts...")
    for _ in range(num_countries):
        country = CapFeedCountry.objects.create(name=fake.country())

        for _ in range(num_admin1s_per_country):
            admin1 = CapFeedAdmin1.objects.create(name=fake.city(), country=country)

            for _ in range(num_alerts_per_admin1):
                sent_time = timezone.now()
                alert = CapFeedAlert.objects.create(sent=sent_time, country=country)
                alert.admin1s.add(admin1)

                CapFeedAlertinfo.objects.create(
                    event=fake.word(),
                    category=fake.word(),
                    urgency="Immediate",
                    severity="Severe",
                    certainty="Likely",
                    alert=alert,
                )


execute_from_command_line(["manage.py", "makemigrations"])
execute_from_command_line(["manage.py", "migrate"])

call_command('flush', '--noinput')

# Create 10 alerts with some variation in countries and admin1s
num_countries = 1
num_admin1s_per_country = 1
num_alerts_per_admin1 = 10

generate_simulated_alert(num_countries, num_admin1s_per_country, num_alerts_per_admin1)

# Generate 10 fake users
generate_fake_users_and_subscriptions(10, 'fake_users.csv', 5)
