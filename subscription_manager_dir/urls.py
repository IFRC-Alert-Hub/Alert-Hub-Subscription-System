from django.urls import path
from . import views

urlpatterns = [
    path('sendmail/', views.send_mail_to_all, name="sendmail"),
    path('get_subscription_alerts/<int:subscription_id>/', views.get_subscirption_alerts,
         name='Get All Alerts Matching Subscriptions'),
]
