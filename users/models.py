# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):  #Comes with built-in user features 
    """
    Custom user model.
    """
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['email','password']

    def __str__(self):
        return f"Welcome {self.username}" 


class UserPreference(models.Model):
    """
    One-to-One relationship.
    Stores the user's favorite genres and languages for recommendations.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")

    preferred_genres = models.JSONField(default=list)  
    preferred_languages = models.JSONField(default=list)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"
