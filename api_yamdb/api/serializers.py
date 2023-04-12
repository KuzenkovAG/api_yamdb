from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Categories, Genre, Titles

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
