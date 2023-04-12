from rest_framework import serializers

from reviews import models


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор Comment."""
    review = serializers.SlugRelatedField(
        slug_field='review',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = models.Comment
