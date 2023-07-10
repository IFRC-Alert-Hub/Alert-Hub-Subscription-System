from django.urls import path
from . import views

urlpatterns = [
    path('sendmail/', views.send_mail_to_all, name="sendmail"),
    path('receive_alert/', views.receive_alert, name="receive packet"),
]
