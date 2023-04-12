import re

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from . import utils
from .mixins import UsernameValidationMixin

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer,
                           UsernameValidationMixin):
    """Serializer for signup user."""
    class Meta:
        fields = ('username', 'email')
        model = User


class TokenObtainSerializer(serializers.Serializer):
    """Serializer for obtain token."""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=256, required=True)

    class Meta:
        fields = ('username', 'confirmation_code')

    def validate_username(self, value):
        get_object_or_404(User, username=value)
        return value

    def validate_confirmation_code(self, value):
        if not re.search(r"\S{6}-\S{32}", value):
            raise serializers.ValidationError(
                'Wrong format of confirmation_code.'
            )
        return value

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not utils.check_confirmation_code(user, confirmation_code):
            raise serializers.ValidationError(
                'Wrong confirmation code.'
            )
        return data


class TokenSerializer(serializers.Serializer):
    """Serializer for token."""
    token = serializers.CharField()


class UsersSerializer(serializers.ModelSerializer, UsernameValidationMixin):
    """Serializer for user."""
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class UserProfileSerializer(UsersSerializer):
    """Serializer for user profile."""
    role = serializers.CharField(read_only=True)
