from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins


User = get_user_model()


class CategoriesViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    pass
