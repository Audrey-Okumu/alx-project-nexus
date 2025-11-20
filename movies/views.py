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


# Get Movie Details
@api_view(["GET"])
def movie_details(request, movie_id):
    try:
        # Try to get from database first
        movie = Movie.objects.filter(tmdb_id=movie_id).first()
        
        if not movie:
            # Fetch from TMDB if not in database
            data = tmdb.get_movie_details(movie_id)
            movie, _ = Movie.objects.get_or_create(
                tmdb_id=data["id"],
                defaults={
                    "title": data.get("title"),
                    "overview": data.get("overview", ""),
                    "poster_url": data.get("poster_path"),
                    "release_date": data.get("release_date"),
                    "genres": [genre["id"] for genre in data.get("genres", [])],
                }
            )

        return Response(MovieSerializer(movie).data)
    
    except Exception as e:
        return Response({"error": f"Failed to fetch movie details: {str(e)}"})

# Search Movies
@api_view(["GET"])
def search_movies(request):
    try:
        query = request.GET.get('query', '').strip()
        if not query:
            return Response({"error": "Query parameter is required"})

        data = tmdb.search_movies(query)
        movies_data = data.get("results", [])

        movies = []
        for item in movies_data:
            movie, _ = Movie.objects.get_or_create(
                tmdb_id=item["id"],
                defaults={
                    "title": item.get("title"),
                    "overview": item.get("overview", ""),
                    "poster_url": item.get("poster_path"),
                    "release_date": item.get("release_date"),
                    "genres": item.get("genre_ids", []),
                }
            )
            movies.append(MovieSerializer(movie).data)

        return Response(movies)
    
    except Exception as e:
        return Response({"error": f"Search failed: {str(e)}"})



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

