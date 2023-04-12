from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins

from reviews.models import Categories, Genre, Titles
import serializers

User = get_user_model()


class CategoriesViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):

    queryset = Categories.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = []


class GenresViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):

    queryset = Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = []


class TitlesViewSet(viewsets.ModelViewSet):

    queryset = Titles.objects.all()
    serializer_class = serializers.TitleSerializer
    permission_classes = []
