"""
URL configuration for movie_backend project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Schema view for automatic Swagger documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Movie Backend API",
        default_version='v1',
        description="""
        Complete Movie API with TMDB integration, user authentication, and favorites management.
        
        ## Features
        - **JWT Authentication** - Secure user authentication
        - **TMDB Integration** - Real movie data from The Movie Database
        - **User Preferences** - Personalized genre and language preferences
        - **Favorites System** - Save and manage favorite movies
        - **Search & Discovery** - Find movies and get recommendations
        
        ## Authentication
        Use the `/api/token/` endpoint to get JWT tokens. Include the token in the Authorization header:
        `Authorization: Bearer <your_access_token>`
        """,
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="akelloaudrey3@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Automatic Swagger UI - drf-yasg provides this automatically
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    path('api/movies/', include('movies.urls')),
]