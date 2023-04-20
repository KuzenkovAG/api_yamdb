import re

from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from . import utils
from .mixins import UsernameValidationMixin
from reviews import models

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category."""
    class Meta:
        fields = ('name', 'slug')
        model = models.Categories


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for Genre."""
    class Meta:
        fields = ('name', 'slug')
        model = models.Genre


class ReadTitleSerializer(serializers.ModelSerializer):
    """Serializer for Title."""
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = models.Title


class TitleSerializer(serializers.ModelSerializer):
    """Serializer for Title."""
    genre = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=models.Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=models.Categories.objects.all()
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = models.Title


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for reviews of titles."""
    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = models.Review
        fields = (
            'id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if models.Review.objects.filter(author=author,
                                        title=title_id).exists():
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


class SignUpSerializer(serializers.Serializer, UsernameValidationMixin):
    """Serializer for signup user."""
    email = serializers.CharField(max_length=254, validators=[validate_email])
    username = serializers.CharField(max_length=150)

    class Meta:
        fields = ('username', 'email')

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        if not User.objects.filter(username=username, email=email).exists():
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    'Username already exists.'
                )
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    'Email already exists.'
                )
        return attrs


class UsersSerializer(serializers.ModelSerializer, UsernameValidationMixin):
    """Serializer for user."""
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User

    def validate_role(self, value):
        if not self.context.get('request').user.is_admin:
            return self.context.get('request').user.role
        return value


class UserProfileSerializer(UsersSerializer):
    """Serializer for user profile."""
    role = serializers.CharField(read_only=True)


class CommentSerializer(serializers.ModelSerializer):
    """Serializer Comment."""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = models.Comment
