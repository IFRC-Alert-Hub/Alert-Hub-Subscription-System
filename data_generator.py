import csv
import os
import django
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'project.production' if 'WEBSITE_HOSTNAME' in os.environ else 'project.settings')
django.setup()

from faker import Faker
import random

from django.db import IntegrityError, transaction
from django.contrib.auth import get_user_model
from subscription_dir.models import Subscription
from subscription_manager_dir.external_alert_models import CapFeedCountry, CapFeedAdmin1

fake = Faker()
User = get_user_model()


def create_user(email, password):
    user = User.objects.create(email=email)
    user.set_password(password)
    user.save()
    return user


def create_subscription(user, country, admin1s):
    return Subscription(
        subscription_name=fake.sentence()[:-1],
        user_id=user.id,
        country_ids=country,
        admin1_ids=admin1s,
        urgency_array=["Immediate"],
        severity_array=["Severe"],
        certainty_array=['Observed', 'Likely', 'Possible'],
        subscribe_by=["Email"],
        sent_flag=3
    )


def generate_fake_users_and_subscriptions(count, csv_filename, country_count, subscription_count):
    users = []

    with open(csv_filename, 'w', newline='') as csvfile:
        fieldnames = ['email', 'password', 'subscription_ids']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        countries = list(CapFeedCountry.objects.filter(id=161))

        with transaction.atomic():
            for i in range(count):
                print("Creating users: {}/{}".format(i + 1, count))
                while True:
                    try:
                        email = fake.unique.email()
                        password = fake.password()

                        user = create_user(email, password)
                        users.append(user)

                        subscriptions_to_create = []
                        subscription_ids = []

                        selected_countries = countries

                        for _ in range(subscription_count):
                            for country in selected_countries:
                                admin1s = CapFeedAdmin1.objects.filter(country=country)
                                if admin1s:
                                    selected_admin1s = random.sample(list(admin1s),
                                                                     random.randint(1,
                                                                                    len(admin1s)))
                                    country_ids = [country.id]
                                    admin1_ids = [admin1.id for admin1 in selected_admin1s]

                                    subscription = create_subscription(user, country_ids,
                                                                       admin1_ids)
                                    subscriptions_to_create.append(subscription)

                        Subscription.objects.bulk_create(subscriptions_to_create)

                        # Retrieve saved subscription IDs
                        subscription_ids = [str(subscription.id) for subscription in
                                            subscriptions_to_create]
                        writer.writerow({'email': email, 'password': password,
                                         'subscription_ids': ', '.join(subscription_ids)})
                        break
                    except IntegrityError as e:
                        print(f"IntegrityError: {e}. Retrying with a different email.")
                        continue
    return users


call_command('flush', '--noinput')

generate_fake_users_and_subscriptions(1000, 'fake_users.csv', 1, 10)