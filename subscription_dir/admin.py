from django.contrib import admin
from .models import User, Region, Subscription

# Register your models here.
admin.site.register(User)
admin.site.register(Region)
admin.site.register(Subscription)
