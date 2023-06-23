# Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory files (.) to the working directory in the container (/app)
ADD . /app

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Upgrade pip and install any needed packages specified in requirements.txt
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt; pylint **/*.py

# Expose port 8000 for the app
EXPOSE 8000

# Collect static files for Django
RUN python manage.py collectstatic --noinput

# Run the Django service when the container launches
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
