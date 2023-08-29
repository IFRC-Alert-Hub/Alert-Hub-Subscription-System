# IFRC/UCL Alert-Hub-Subscription-System

## Description

This project serves as a back-end application of IFRC Alert Hub designed to work with [IFRC/UCL
Alert Hub CAP Aggregator](https://github.com/IFRC-Alert-Hub/Alert-Hub-CAP-Aggregator).
This application relies on it to get real-time updates about alerts.

Additionally, this back-end project is designed to work with a corresponding front-end application.
You can find the front-end code at [https://github.com/IFRC-Alert-Hub/Alert-Hub-Frontend].

The goal of the IFRC Alert Hub is to ensure that communities around the world receive the most
timely and effective emergency alerts possible, so that action can be taken to protect their lives
and livelihoods.

## Features

- A global alert map: Offers a geospatial overview of worldwide emergencies.
- User subscription system: Allows personalized accounts and subscriptions to regions or disaster
  severities of interest.
- Email notifications: Sends real-time updates on emergencies to users based on their subscription.

## Installation and Usage

### Prerequisites

Before you start, make sure you have:

- Python 3.9 or higher: Download it from [here](https://www.python.org/downloads/) and install
  it on your system.
- PostgreSQL: This project uses PostgreSQL as its database. You can download it from [here]
  (https://www.postgresql.org/download/) and find the installation
  guide [here](https://www.postgresql.org/docs/10/installation.html).
- RabbitMQ: This project uses RabbitMQ for its message broker. You can download it
  from [here](https://www.rabbitmq.com/download.html) and find the installation
  guide [here](https://www.rabbitmq.com/install-guide.html).
- CAP Aggregator: This project also relies on
  the [IFRC/UCL Alert Hub CAP Aggregator](https://github.com/IFRC-Alert-Hub/Alert-Hub-CAP-Aggregator).
  Make sure the CAP Aggregator is correctly installed and running.
- Redis (Recommend 7.0.12 or higher): This project uses Redis to store tasks for Celery tasks. 
  You can find the installation guide from [here](https://redis.io/docs/getting-started/installation/).

### Run the Application

1. Clone the repository to your local machine:

```bash
https://github.com/IFRC-Alert-Hub/Alert-Hub-Backend.git
```

2. Navigate into the project directory:

```bash
cd Alert-Hub-Subscription-System
```

3. Install the Python dependencies from the requirements.txt file:

```bash
pip install -r requirements.txt
```

4. Configure the Django application:

```bash
python manage.py migrate
python manage.py createcachetable
python manage.py collectstatics
```

5. Configure the postgreSQL database, the rabbitmq server and the websocket in .env file
```
SUBSCRIPTION_POSTGRESQL_CONNECTIONSTRING=dbname=cap_alert host=localhost port=5432 sslmode=require user=1234 password=1234
ALERT_POSTGRESQL_CONNECTIONSTRING=dbname=cap_aggregator host=localhost port=5432 sslmode=require user=postgres password=1234
SECRET_KEY=1187ee740a5e11ef86a3df5e50df7d04dd61539de55bcc7facd6faa3c2ee69e3
DEBUG=True
CELERY_BROKER_URL=redis://:@localhost:6379/3
REDIS_URL=redis://localhost:6379/1
DBBACKUP_STORAGE='dbbackup.storage.filesystem_storage'
TEST_MODE=True
```

6. Start the redis server:
```bash
redis-server
```

7. Start the server:
```bash
python manage.py runserver
```

8. Start celery worker and scheduler:
```bash
celery -A project worker -l info --pool=solo
celery -A project beat -l info
```

## Access the admin page

Django provides us Admin Panel for it’s users. 
So we need not worry about creating a separate Admin page or providing authentication feature 
as Django provides us that feature. 
Before using this feature, you must have migrated your project, otherwise the superuser database will not be created.

1. You should create superuser, first reach the same directory as that of manage.py and run the following command:
```bash
python manage.py createsuperuser
```

2. You can access the admin page 
   from [here] (http://127.0.0.1:8000/admin/login/?next=/admin/)

## Access the GraphQL page

In this project, we use GraphQL to access the interfaces provided from the backend.
You can access the GraphQL page by getting urls from urls.py

```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin')),
    path('users/', include('user_dir.urls')),
    path('subscription/', include('subscription_dir.urls')),
    path('subscription_manager/', include('subscription_manager_dir.urls')),
    path('health_check/', include('health_check.urls'))
]
```

For example, you can access the subscription GraphQL page 
by this [url](http://127.0.0.1:8000/subscription/graphql).

To make sure that the GraphQL page can be accessed via a web page,
you should set the graphiql as True in urls.py.
```
urlpatterns = [
    # ...
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]
```

## Devops Operations

### Health Check Endpoint

To ensure service availability, the following endpoint can be leveraged for health check:

```bash
http://$HOST:$PORT/health_check/
```

More description can be referred from [health check description](documents/health_check.md).

You can integrate this endpoint with Cloud service like Azure, AWS.

### DB Backup

To ensure data availability, the database can be backup and restored by following command:

1. Run backup
```bash
python manage.py dbbackup
```

2. Restore from backup
```bash
python manage.py dbrestore
```

More description can be referred from [dbbackup description](documents/dbbackup.md).

You can integrate this backup service with Linux crontab service, 
or Cloud service like Azure, AWS.

## Datasources
Our datasources of boundaries of administrative areas come from [GADM data](https://gadm.org/data.html).

## Design Documentation
Our design documentations are stored in [Google Drive](https://drive.google.com/drive/folders/1nMoEtwBAnaMjTywjXBGRNS1OZD4mPgUo).
