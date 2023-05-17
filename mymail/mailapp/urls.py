from django.urls import path
from . import views

app_name = "mailapp"

urlpatterns = [
    path('', views.index, name='index'),
    path('mails/', views.receive_emails, name='mails'),
    path('success/', views.send_email, name='send_mail'),
]