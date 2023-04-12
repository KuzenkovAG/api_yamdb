from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from reviews.models import Review

from .permissions import (IsAdminPermission,
                          IsModeratorPermission,
                          IsAuthorPermission)
from .serializers import  CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminPermission,
                          IsModeratorPermission,
                          IsAuthorPermission]

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
