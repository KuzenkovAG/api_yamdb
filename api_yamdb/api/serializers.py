from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from . import utils

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
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
    confirmation_code = serializers.CharField(max_length=256)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User

    def validate(self, attrs):
        username = self.data.get('username')
        confirmation_code = self.data.get('confirmation_code')
        user = get_object_or_404(User, username=username)
        if not utils.check_confirmation_code(user, confirmation_code):
            raise serializers.ValidationError(
                'Wrong confirmation code.'
            )


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()
