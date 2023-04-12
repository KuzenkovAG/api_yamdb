from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet
from reviews.models import Titles

router = DefaultRouter()
router.register('categories', CategoriesViewSet)
router.register('genres', GenresViewSet)
router.register(
    'titles',
    TitlesViewSet,
    basename=Titles
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
