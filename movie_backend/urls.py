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
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

#  Custom Swagger UI view
def custom_swagger_view(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Movie Backend API - Swagger UI</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui.css">
        <style>
            html { box-sizing: border-box; overflow-y: scroll; }
            *, *:before, *:after { box-sizing: inherit; }
            body { margin: 0; background: #fafafa; }
            .swagger-ui .topbar { display: none; }
            #swagger-ui { padding: 20px; }
            .auth-container { margin: 20px; }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui-standalone-preset.js"></script>
        <script>
        window.onload = function() {
            try {
                const ui = SwaggerUIBundle({
                    url: '/swagger.json',
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    plugins: [
                        SwaggerUIBundle.plugins.DownloadUrl
                    ],
                    layout: "StandaloneLayout",
                    validatorUrl: null,
                    displayRequestDuration: true,
                    docExpansion: 'none',
                    // Add request interceptor to ensure Authorization header is sent
                    requestInterceptor: (request) => {
                        // Ensure Authorization header is properly formatted
                        if (request.headers.Authorization && !request.headers.Authorization.startsWith('Bearer ')) {
                            request.headers.Authorization = 'Bearer ' + request.headers.Authorization;
                        }
                        return request;
                    }
                });
                
                // Add authorization header to all requests
                ui.getConfigs().requestInterceptor = function(request) {
                    if (request.headers.Authorization && !request.headers.Authorization.startsWith('Bearer ')) {
                        request.headers.Authorization = 'Bearer ' + request.headers.Authorization;
                    }
                    return request;
                };
                
                console.log('Swagger UI loaded successfully');
            } catch (error) {
                console.error('Swagger UI error:', error);
                document.getElementById('swagger-ui').innerHTML = 
                    '<h1>Error loading Swagger UI</h1><p>' + error.message + '</p>';
            }
        };
        </script>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    # Home page - Fixed Custom Swagger UI
    path('', custom_swagger_view),
    
    # Alternative paths
    path('swagger/', custom_swagger_view),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # Admin
    path('admin/', admin.site.urls),
    
    # API Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users/', include('users.urls')),
    path('api/movies/', include('movies.urls')),
]