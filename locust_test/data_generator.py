import csv
import os

import django

if 'WEBSITE_HOSTNAME' in os.environ:
    settings_module = "project.production"
else:
    settings_module = "project.settings"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

# Configure Django settings
django.setup()

from faker import Faker
import random

from django.core.management import call_command, execute_from_command_line
from django.contrib.auth import get_user_model
from subscription_dir.models import Subscription
from subscription_manager_dir.external_alert_models import CapFeedCountry, CapFeedAdmin1

fake = Faker()
User = get_user_model()


def create_user(email, password):
    user = User.objects.create(
        email=email,
    )
    user.set_password(password)
    user.save()
    return user


def create_subscription(user, country, admin1s):
    return Subscription.objects.create(
        subscription_name=fake.sentence()[:-1],
        user_id=user.id,
        country_ids=country,
        admin1_ids=admin1s,
        urgency_array=["Immediate"],
        severity_array=["Severe"],
        certainty_array=['Observed', 'Likely', 'Possible'],
        subscribe_by=["Email"],
        sent_flag=0,
    )


def generate_fake_users_and_subscriptions(count, csv_filename, country_count):
    users = []

    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['email', 'password', 'subscription_ids']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        countries = list(CapFeedCountry.objects.all())

        for i in range(count):
            print("Creating users: {}/{}".format(i + 1, count))
            email = fake.email()
            password = fake.password()

            user = create_user(email, password)
            users.append(user)

            subscriptions = []
            selected_countries = random.sample(countries, country_count)

            for country in selected_countries:
                admin1s = CapFeedAdmin1.objects.filter(country=country)

                if admin1s:  # Check if admin1s is not empty
                    selected_admin1s = random.sample(list(admin1s), random.randint(1, len(admin1s)))

                    country_ids = [country.id]
                    admin1_ids = [admin1.id for admin1 in selected_admin1s]

                    subscription = create_subscription(user, country_ids, admin1_ids)
                    subscriptions.append(str(subscription.id))

                    subscription_ids = ', '.join(subscriptions)

            writer.writerow(
                {'email': email, 'password': password, 'subscription_ids': subscription_ids})

    return users


call_command('flush', '--noinput')

# Generate 10 fake users
generate_fake_users_and_subscriptions(10, 'fake_users.csv', 5)
