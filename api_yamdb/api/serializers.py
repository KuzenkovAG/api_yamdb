import re

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from . import utils
from .mixins import UsernameValidationMixin
from reviews.models import Review, Categories, Genre, Titles

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):

    name = serializers.StringRelatedField()
    slug = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Categories


class GenreSerializer(serializers.ModelSerializer):

    name = serializers.StringRelatedField()
    slug = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Genre


class GenreSerializer(serializers.ModelSerializer):

    name = serializers.StringRelatedField()
    slug = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Genre


class TitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Titles


class ReviewSerializer(serializers.ModelSerializer):

    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение'
            )
        return data


class TokenObtainSerializer(serializers.Serializer):
    """Serializer for obtain token."""
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=256, required=True)

    class Meta:
        fields = ('username', 'confirmation_code')

    @staticmethod
    def validate_username(value):
        get_object_or_404(User, username=value)
        return value

    @staticmethod
    def validate_confirmation_code(value):
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


class UserCreateSerializer(serializers.ModelSerializer,
                           UsernameValidationMixin):
    """Serializer for signup user."""
    class Meta:
        fields = ('username', 'email')
        model = User


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
