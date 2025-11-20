# movie_backend/views.py
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "message": "Movie Backend API",
        "endpoints": {
            "users": {
                "preferences": "/users/preferences/",
                "update_preferences": "/users/preferences/update/"
            },
            "movies": {
                "trending": "/movies/trending/",
                "search": "/movies/search/?query=avengers",
                "movie_details": "/movies/550/",
                "recommendations": "/movies/550/recommended/",
                "add_favorite": "/movies/550/favorite/",
                "list_favorites": "/movies/favorites/",
                "remove_favorite": "/movies/favorites/550/remove/"
            },
            "authentication": {
                "login": "/api-auth/login/",
                "logout": "/api-auth/logout/"
            }
        }
    })