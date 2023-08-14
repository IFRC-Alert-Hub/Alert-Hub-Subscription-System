from django.urls import path
from . import views

urlpatterns = [
    path('get_subscription_alerts/<int:subscription_id>/', views.get_subscirption_alerts,
         name='Get All Alerts Matching Subscriptions'),
]
