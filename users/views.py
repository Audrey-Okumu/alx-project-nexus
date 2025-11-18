from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import UserPreference
from .serializers import UserPreferenceSerializer

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
