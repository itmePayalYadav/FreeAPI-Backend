from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    """For safe user responses (no password)"""
    class Meta:
        model = User
        fields = ["id", "username", "email", "is_premium", "avatar", "email_verified", "is_superuser", "is_staff", "is_active"]

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password], min_length=6)

    class Meta:
        model = User
        fields = ["username", "email", "password", "is_premium"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            is_premium=validated_data.get("is_premium", False)
        )
        return user
