from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins

from .serializers import CategorySerializer


User = get_user_model()


class CategoriesViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):

    serializer_class = CategorySerializer
