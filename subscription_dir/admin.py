from django.contrib import admin

# Register your models here.
from .models import Alert,AlertInfo,Country, Region
admin.site.register(Alert)
admin.site.register(AlertInfo)
admin.site.register(Region)
admin.site.register(Country)