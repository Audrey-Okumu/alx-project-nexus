"""
URL configuration for movie_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""
URL configuration for movie_backend project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Schema view for JSON
schema_view = get_schema_view(
    openapi.Info(
        title="Movie Backend API",
        default_version='v1',
        description="Movie API with TMDB integration and JWT authentication",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Simple home page view
def home_view(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Movie Backend API</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            .container { text-align: center; }
            .btn { display: inline-block; padding: 10px 20px; margin: 10px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }
            .api-list { text-align: left; margin: 30px 0; }
            .endpoint { background: #f8f9fa; padding: 10px; margin: 5px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1> Movie Backend API</h1>
            <p> Backend working fine!</p>
            <p>Your Django API is successfully deployed on Railway.</p>
            
            <div class="api-list">
                <h3> Available Endpoints:</h3>
                <div class="endpoint"><strong>GET</strong> /api/movies/trending/ - Trending movies</div>
                <div class="endpoint"><strong>GET</strong> /api/movies/search/?query=inception - Search movies</div>
                <div class="endpoint"><strong>GET</strong> /api/movies/123/ - Movie details</div>
                <div class="endpoint"><strong>POST</strong> /api/users/register/ - Register user</div>
                <div class="endpoint"><strong>POST</strong> /api/token/ - Login & get JWT tokens</div>
            </div>
            
            <div>
                <a href="/swagger/" class="btn">View Swagger Documentation</a>
                <a href="/api/movies/trending/" class="btn">Test Trending Movies</a>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    # Home page - Simple HTML page
    path('', home_view, name='home'),
    
    # Swagger URLs - Use DRF Yasg's built-in view
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Endpoints 
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    path('api/movies/', include('movies.urls')),
]