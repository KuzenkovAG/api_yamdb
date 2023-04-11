import re

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from . import utils

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for signup user."""
    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Username should be not equal "me"'
            )
        return value


class TokenObtainSerializer(serializers.ModelSerializer):
    """Serializer for obtain token."""
    confirmation_code = serializers.CharField(max_length=256, required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User

    def validate_username(self, value):
        get_object_or_404(User, username=value)
        return value

    def validate_confirmation_code(self, value):
        if not re.search(r"\S{6}-\S{32}", value):
            raise serializers.ValidationError(
                'Wrong format of confirmation_code.'
            )
        return value

    def validate(self, attrs):
        username = self.data.get('username')
        confirmation_code = self.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not utils.check_confirmation_code(user, confirmation_code):
            raise serializers.ValidationError(
                'Wrong confirmation code.'
            )


class TokenSerializer(serializers.Serializer):
    """Serializer for token."""
    token = serializers.CharField()
