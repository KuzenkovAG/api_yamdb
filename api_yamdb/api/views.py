import json

from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import exceptions, filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    SAFE_METHODS
)
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Avg

from . import permissions
from . import serializers
from . import utils
from .filters import TitleFilter
from reviews import models

User = get_user_model()


class CategoryGenreBaseViewSet(viewsets.ModelViewSet):
    """Base viewset for category and genre."""
    permission_classes = [permissions.IsAdminOrReadPermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'

    def get_object(self):
        if self.request.method != 'DELETE':
            raise exceptions.MethodNotAllowed(self.request.method)
        return super().get_object()


class CategoriesViewSet(CategoryGenreBaseViewSet):
    """Viewset for Category."""
    queryset = models.Categories.objects.all()
    serializer_class = serializers.CategorySerializer


class GenresViewSet(CategoryGenreBaseViewSet):
    """Viewset for Genre."""
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset for Title."""
    queryset = models.Title.objects.annotate(
        rating=Avg('reviews__score')).all().order_by('name')
    serializer_class = serializers.TitleSerializer
    permission_classes = [permissions.IsAdminOrReadPermission]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return serializers.ReadTitleSerializer
        return serializers.TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Working with reviews."""
    serializer_class = serializers.ReviewSerializer
    permission_classes = [permissions.AdminOrModeratorOrAuthorPermission]

    def get_queryset(self):
        title = get_object_or_404(models.Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(models.Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


@api_view(['POST'])
def send_confirmation_mail(request):
    """Send confirmation mail. If user not exist, create user."""
    serializer = serializers.SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, _ = User.objects.get_or_create(
        username=request.data.get('username'),
        email=request.data.get('email')
    )
    utils.send_email_with_confirmation_code(user)
    return Response(request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@csrf_exempt
def receive_token(request):
    """Receive token by confirmation code."""
    serializer = serializers.TokenObtainSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data.get('username'))
    token = RefreshToken.for_user(user)
    json_data = json.dumps({'token': str(token.access_token)})
    return Response(json_data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Viewset for User."""
    serializer_class = serializers.UsersSerializer
    permission_classes = [IsAuthenticated & (
        permissions.IsAdminPermission | IsAdminUser
    )]
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated, ]
    )
    def me(self, request):
        user = get_object_or_404(User, id=request.user.id)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset for the Comment model."""
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.AdminOrModeratorOrAuthorPermission]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(models.Review,
                                   id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(models.Review,
                                   id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
