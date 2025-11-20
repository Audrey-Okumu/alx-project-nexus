from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from .models import UserPreference
from .serializers import UserPreferenceSerializer,  UserSerializer

User = get_user_model()

#  User Registration
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user and return JWT tokens
    POST /users/register/
    {
        "username": "testuser",
        "email": "test@example.com", 
        "password": "testpass123"
    }
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Create user preferences
        UserPreference.objects.create(user=user)
        
        # Generate JWT tokens
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

#  Get Current User Profile
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    Get current authenticated user profile
    GET /users/profile/
    Header: Authorization: Bearer <access_token>
    """
    return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email
    })

# Get user preferences

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_preferences(request):
    prefs, _ = UserPreference.objects.get_or_create(user=request.user)
    return Response(UserPreferenceSerializer(prefs).data)

#Update preferences

@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_preferences(request):
    prefs, _ = UserPreference.objects.get_or_create(user=request.user)
    serializer = UserPreferenceSerializer(prefs, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)
