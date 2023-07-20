from django.db import models


class Polygon(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(default=0, verbose_name="user_id")
    vertices = models.CharField(default="None")
