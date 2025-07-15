from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("readfile_to_n8n", views.readfile_to_n8n, name="readfile_to_n8n"),
]
