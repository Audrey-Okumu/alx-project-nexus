# users/models.py
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    """
    Custom user model.
    Django requires overriding groups and permissions to avoid clashes.
    """
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",
        blank=True
    )

    REQUIRED_FIELDS = ['email', 'password']

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
