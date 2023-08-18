from locust import HttpUser, task
import csv

class SubscriptionUser(HttpUser):
    @task
    def read_csv_and_send_requests(self):
        with open('fake_users.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                subscription_ids = row['subscription_ids'].split(',')
                for subscription_id in subscription_ids:
                    url = f"https://backend-deploy.azurewebsites.net/subscription_manager/get_subscription_alerts/{subscription_id}/"
                    self.client.get(url)

