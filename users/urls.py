from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register_user, name="register"),
    path("profile/", views.get_profile, name="profile"),
    path("preferences/", views.get_preferences, name="get_preferences"),
    path("preferences/update/", views.update_preferences, name="update_preferences"),
]