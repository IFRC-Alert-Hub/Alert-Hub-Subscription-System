# IFRC/UCL Alert Hub backend

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
- Redis: This project uses redis for its message broker.
- CAP Aggregator: This project also relies on
  the [IFRC/UCL Alert Hub CAP Aggregator](https://github.com/IFRC-Alert-Hub/Alert-Hub-CAP-Aggregator).
  Make sure the CAP Aggregator is correctly installed and running.

### Install Application Dependencies

1. Clone the repository to your local machine:

```bash
https://github.com/IFRC-Alert-Hub/Alert-Hub-Backend.git
```

2. Navigate into the project directory:

```bash
cd Alert-Hub-Backend
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

5. Configure the postgreSQL database, the rabbitmq server and the websocket

6. Start the server:

```bash
python manage.py runserver
```

7. Start celery worker and sceduler:

```bash
celery -A project worker -l info --pool=solo
celery -A project beat -l info
```

## Docker Deployment

### Prerequisites

Ensure you have the following installed on your machine:

- Docker: This is required to create and manage your application's containers. If Docker is not
  already installed, follow the guide here to install Docker.
- Docker Compose: This is required to manage your application's services. It's usually included
  with Docker. If not, follow the guide here to install Docker Compose.

### Building the Docker Image and Running the Containers

1. Clone the repository to your local machine:

```bash
git clone https://github.com/IFRC-Alert-Hub/Alert-Hub-Backend.git
```

2. Navigate into the project directory:

```bash
cd Alert-Hub-Backend
```

3. Build and run the Docker containers:

```bash
docker-compose up --build
```

This command builds the Docker images if they don't exist and starts the containers. If the images
already exist, it just starts the containers.

To ensure that the Docker containers are running, you can run docker ps which lists all running
Docker containers.

### Stopping the Docker Containers
To stop the Docker containers, run the following command:
```bash
docker-compose down
```

You can either use [Docker Desktop](https://www.docker.com/products/docker-desktop/) to manage 
your containers.