# movies/services/movie_sync.py
from .tmdb import TMDBClient
from movies.models import Movie


def sync_movie_from_tmdb(tmdb_movie):
    """
    Saves a TMDB movie response into the local DB.
    If already exists, update it.
    """
    movie, created = Movie.objects.update_or_create(
        tmdb_id=tmdb_movie["id"],
        defaults={
            "title": tmdb_movie.get("title"),
            "overview": tmdb_movie.get("overview"),
            "poster_url": f'https://image.tmdb.org/t/p/w500{tmdb_movie.get("poster_path")}'
            if tmdb_movie.get("poster_path")
            else None,
            "release_date": tmdb_movie.get("release_date") or None,
            "genres": tmdb_movie.get("genre_ids", []),
            "language": tmdb_movie.get("original_language", "en"),
        },
    )

    return movie
