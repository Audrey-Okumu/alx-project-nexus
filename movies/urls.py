from django.urls import path
from . import views

urlpatterns = [
    path("trending/", views.trending_movies),
    path("search/", views.search_movies),  # ✅ ADD THIS
    path("<int:movie_id>/", views.movie_details),  # ✅ ADD THIS
    path("<int:movie_id>/recommended/", views.recommended_movies),
    path("<int:movie_id>/favorite/", views.add_favorite),
    path("favorites/", views.list_favorites),
    path("favorites/<int:movie_id>/remove/", views.remove_favorite),
]