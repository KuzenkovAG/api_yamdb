from django.contrib.auth import get_user_model
from rest_framework import serializers

from reviews.models import Categories

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )
    slug = serializers.SlugRelatedField(
        read_only=True,
        slug_field='slug',
    )

    class Meta:
        fields = '__all__'
        model = Categories
