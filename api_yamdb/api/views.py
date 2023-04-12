from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions

from reviews import models
from . import permissions
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          permissions.IsAdminPermission,
                          permissions.IsModeratorPermission,
                          permissions.IsAuthorPermission]

    def get_queryset(self):
        review = get_object_or_404(models.Review,
                                   id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(models.Review,
                                   id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
