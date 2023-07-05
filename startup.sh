python manage.py migrate
celery -A project worker -l info --pool=solo & celery -A project beat -l info