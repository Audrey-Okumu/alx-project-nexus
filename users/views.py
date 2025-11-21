from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from .models import UserPreference
from .serializers import UserPreferenceSerializer,  UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

# User Registration
@swagger_auto_schema(
    method='post',
    operation_summary="Register new user",
    operation_description="Create a new user account and receive JWT tokens",
    request_body=UserSerializer,
    responses={
        201: openapi.Response(
            description="User created successfully",
            examples={
                "application/json": {
                    "message": "User created successfully",
                    "user": {
                        "id": 1,
                        "username": "testuser",
                        "email": "test@example.com"
                    },
                    "tokens": {
                        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
                        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
                    }
                }
            }
        ),
        400: openapi.Response(description="Invalid input data")
    }
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        UserPreference.objects.create(user=user)
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Get User Profile
@swagger_auto_schema(
    method='get',
    operation_summary="Get user profile",
    operation_description="Retrieve current authenticated user's profile information",
    responses={
        200: openapi.Response(
            description="User profile data",
            examples={
                "application/json": {
                    "id": 1,
                    "username": "testuser",
                    "email": "test@example.com"
                }
            }
        ),
        401: openapi.Response(description="Authentication required")
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
    })

# Get User Preferences
@swagger_auto_schema(
    method='get',
    operation_summary="Get user preferences",
    operation_description="Retrieve user's preferred genres and languages",
    responses={
        200: UserPreferenceSerializer,
        401: openapi.Response(description="Authentication required")
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_preferences(request):
    prefs, _ = UserPreference.objects.get_or_create(user=request.user)
    return Response(UserPreferenceSerializer(prefs).data)

# Update User Preferences
@swagger_auto_schema(
    method='put',
    operation_summary="Update user preferences",
    operation_description="Update user's preferred genres and languages",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'preferred_genres': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_INTEGER),
                description="List of genre IDs"
            ),
            'preferred_languages': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(type=openapi.TYPE_STRING),
                description="List of language codes (en, es, fr, etc.)"
            )
        }
    ),
    responses={
        200: UserPreferenceSerializer,
        400: openapi.Response(description="Invalid input data"),
        401: openapi.Response(description="Authentication required")
    }
)
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_preferences(request):
    prefs, _ = UserPreference.objects.get_or_create(user=request.user)
    serializer = UserPreferenceSerializer(prefs, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)