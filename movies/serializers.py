from rest_framework import serializers
from .models import Movie, FavoriteMovie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class FavoriteMovieSerializer(serializers.ModelSerializer):
    movie = MovieSerializer(read_only=True)

    class Meta:
        model = FavoriteMovie
        fields = ["id", "movie", "added_at"]
