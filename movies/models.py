# movies/models.py
from django.db import models
from users.models import User


class Movie(models.Model):
    """
    Movies stored locally after fetching from TMDB.
    Ensures we have a stable reference for favorites.
    """
    tmdb_id = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    overview = models.TextField(blank=True)
    poster_url = models.URLField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    genres = models.JSONField(default=list)
    language = models.CharField(max_length=10, default="en")

    def __str__(self):
        return self.title


class FavoriteMovie(models.Model):
    """
    Join table for User <-> Movie (Many-to-Many).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="favorited_by")

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'movie')  # A user can't favorite the same movie twice

    def __str__(self):
        return f"{self.user.username} → {self.movie.title}"
