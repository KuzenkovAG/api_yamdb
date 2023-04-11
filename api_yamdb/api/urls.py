from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CategoriesViewSet
from reviews.models import Categories

router = DefaultRouter()
router.register(
    'categories',
    CategoriesViewSet,
    basename=Categories
)


urlpatterns = [
    path('v1/', include(router.urls)),
]
