from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.shortcuts import get_object_or_404

from .models import Movie, FavoriteMovie
from .serializers import MovieSerializer, FavoriteMovieSerializer
from .services.tmdb import TMDBClient

tmdb = TMDBClient()

CACHE_TIMEOUT = 60 * 60  # 1 hour

# Helper function to build full poster URL
def build_poster_url(poster_path):
    if poster_path:
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

#Get Trending Movies (cached + auto-save to DB)

@api_view(["GET"])
def trending_movies(request):
  try:
    cached = cache.get("trending_movies")  #check cache

    if cached:
        return Response(cached)

    data = tmdb.get_trending_movies() #Fetch from TMDB API
    movies_data = data.get("results", [])

    movies = []
    for item in movies_data:
        movie, _ = Movie.objects.get_or_create(
            tmdb_id=item["id"],
            defaults={
                "title": item.get("title"),
                "overview": item.get("overview"),
                "poster_url": build_poster_url(item.get("poster_path")), 
                "release_date": item.get("release_date"),
                "genres": item.get("genre_ids", []),
            }
        )
        movies.append(MovieSerializer(movie).data)

    cache.set("trending_movies", movies, CACHE_TIMEOUT)

    return Response(movies)
  except Exception as e:
        return Response({"error": f"Failed to fetch trending movies: {str(e)}"}, status=500)

# Get Movie Recommendations
@api_view(["GET"])
def recommended_movies(request, movie_id):
    try:
        data = tmdb.get_recommended(movie_id)
        movies_data = data.get("results", [])

        movies = []
        for item in movies_data:
            movie, _ = Movie.objects.get_or_create(
                tmdb_id=item["id"],
                defaults={
                    "title": item.get("title"),
                    "overview": item.get("overview", ""),
                    "poster_url": build_poster_url(item.get("poster_path")),  # ✅ FIXED
                    "release_date": item.get("release_date"),
                    "genres": item.get("genre_ids", []),
                }
            )
            movies.append(MovieSerializer(movie).data)

        return Response(movies)
    
    except Exception as e:
        return Response({"error": f"Failed to fetch recommendations: {str(e)}"}, status=500)

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
                    "poster_url": build_poster_url(data.get("poster_path")),  # ✅ FIXED
                    "release_date": data.get("release_date"),
                    "genres": [genre["id"] for genre in data.get("genres", [])],
                }
            )

        return Response(MovieSerializer(movie).data)
    
    except Exception as e:
        return Response({"error": f"Failed to fetch movie details: {str(e)}"}, status=500)

# Search Movies
@api_view(["GET"])
def search_movies(request):
    try:
        query = request.GET.get('query', '').strip()
        if not query:
            return Response({"error": "Query parameter is required"}, status=400)

        data = tmdb.search_movies(query)
        movies_data = data.get("results", [])

        movies = []
        for item in movies_data:
            movie, _ = Movie.objects.get_or_create(
                tmdb_id=item["id"],
                defaults={
                    "title": item.get("title"),
                    "overview": item.get("overview", ""),
                    "poster_url": build_poster_url(item.get("poster_path")),  # ✅ FIXED
                    "release_date": item.get("release_date"),
                    "genres": item.get("genre_ids", []),
                }
            )
            movies.append(MovieSerializer(movie).data)

        return Response(movies)
    
    except Exception as e:
        return Response({"error": f"Search failed: {str(e)}"}, status=500)

# Add to favorites
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_favorite(request, movie_id):
    try:
        user = request.user
        
        # Try to get movie from local database first
        movie = Movie.objects.filter(id=movie_id).first()
        
        # If movie doesn't exist locally, fetch from TMDB
        if not movie:
            try:
                # Fetch movie details from TMDB
                tmdb_data = tmdb.get_movie_details(movie_id)
                
                # Create the movie in local database
                movie, created = Movie.objects.get_or_create(
                    tmdb_id=tmdb_data["id"],
                    defaults={
                        "title": tmdb_data.get("title"),
                        "overview": tmdb_data.get("overview", ""),
                        "poster_url": build_poster_url(tmdb_data.get("poster_path")),
                        "release_date": tmdb_data.get("release_date"),
                        "genres": [genre["id"] for genre in tmdb_data.get("genres", [])],
                    }
                )
            except Exception as e:
                return Response({"error": f"Movie not found in TMDB: {str(e)}"}, status=404)

        # add to favorites
        fav, created = FavoriteMovie.objects.get_or_create(
            user=user,
            movie=movie
        )

        if not created:
            return Response({"message": "Already in favorites"})

        return Response(FavoriteMovieSerializer(fav).data)
    
    except Exception as e:
        return Response({"error": f"Failed to add favorite: {str(e)}"}, status=500)

# List favorite movies
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_favorites(request):
    try:
        favs = FavoriteMovie.objects.filter(user=request.user).select_related('movie')
        return Response(FavoriteMovieSerializer(favs, many=True).data)
    
    except Exception as e:
        return Response({"error": f"Failed to fetch favorites: {str(e)}"}, status=500)

# Remove from favorites
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def remove_favorite(request, movie_id):
    try:
        deleted_count, _ = FavoriteMovie.objects.filter(
            user=request.user,
            movie_id=movie_id
        ).delete()

        if deleted_count == 0:
            return Response({"message": "Movie not found in favorites"}, status=404)

        return Response({"message": "Removed from favorites"})
    
    except Exception as e:
        return Response({"error": f"Failed to remove favorite: {str(e)}"}, status=500)