from django.db import models
from django.db.models import JSONField


class Alerts(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    country_name = models.CharField(max_length=255)
    country_id = models.CharField(max_length=255)
    source_feed = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
    urgency = models.CharField(max_length=255)
    severity = models.CharField(max_length=255)
    certainty = models.CharField(max_length=255)
    info = JSONField()
    user = models.ForeignKey(
        "user_dir.CustomUser",
        related_name="alerts",
        on_delete=models.CASCADE
    )
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
