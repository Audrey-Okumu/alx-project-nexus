from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache

from .models import Movie, FavoriteMovie
from .serializers import MovieSerializer, FavoriteMovieSerializer
from .services.tmdb import TMDBClient

tmdb = TMDBClient()

CACHE_TIMEOUT = 60 * 60  # 1 hour

#Get Trending Movies (cached + auto-save to DB)

@api_view(["GET"])
def trending_movies(request):
    cached = cache.get("trending_movies")  #check cache

    if cached:
        return Response(cached)

    data = tmdb.get_trending_movies()["results"] #Fetch from TMDB API

    movies = []
    for item in data:
        movie, _ = Movie.objects.get_or_create(
            tmdb_id=item["id"],
            defaults={
                "title": item.get("title"),
                "overview": item.get("overview"),
                "poster_url": item.get("poster_path"),
                "release_date": item.get("release_date"),
                "genres": item.get("genre_ids", []),
            }
        )
        movies.append(MovieSerializer(movie).data)

    cache.set("trending_movies", movies, CACHE_TIMEOUT)

    return Response(movies)

#Get Movie Recommendations
@api_view(["GET"])
def recommended_movies(request, movie_id):
    data = tmdb.get_recommended(movie_id)["results"]

    movies = []
    for item in data:
        movie, _ = Movie.objects.get_or_create(
            tmdb_id=item["id"],
            defaults={
                "title": item.get("title"),
                "overview": item.get("overview"),
                "poster_url": item.get("poster_path"),
                "genres": item.get("genre_ids", []),
            }
        )
        movies.append(MovieSerializer(movie).data)

    return Response(movies)

#Add to favorites

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_favorite(request, movie_id):
    user = request.user

    movie = Movie.objects.get(pk=movie_id)

    fav, created = FavoriteMovie.objects.get_or_create(
        user=user,
        movie=movie
    )

    if not created:
        return Response({"message": "Already in favorites"})

    return Response(FavoriteMovieSerializer(fav).data)

#List favorite movies

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    favs = FavoriteMovie.objects.filter(user=request.user)
    return Response(FavoriteMovieSerializer(favs, many=True).data)

#Remove from favorites

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_favorite(request, movie_id):
    FavoriteMovie.objects.filter(
        user=request.user,
        movie_id=movie_id
    ).delete()

    return Response({"message": "Removed"})

