from django.urls import path
from . import views

urlpatterns = [
    path("preferences/", views.get_preferences),
    path("preferences/update/", views.update_preferences),
]
