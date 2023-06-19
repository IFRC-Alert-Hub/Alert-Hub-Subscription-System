from django.contrib import admin

# Register your models here.
from .models import Alert,AlertInfo
admin.site.register(Alert)
admin.site.register(AlertInfo)