from django.db import models

# Create your models here.
class alert(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    integer = models.IntegerField()
    creation_date = models.TimeField()
