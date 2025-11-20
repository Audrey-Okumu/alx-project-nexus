from rest_framework import serializers
from django.contrib.auth import get_user_model  
from .models import UserPreference

User = get_user_model()  # gets custom User model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreference
        fields = "__all__"
        read_only_fields = ['user', 'created_at']