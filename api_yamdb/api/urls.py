from django.urls import include, path
from rest_framework.routers import SimpleRouter

import views
from reviews.models import Titles

router = SimpleRouter()
router.register('categories', views.CategoriesViewSet)
router.register('genres', views.GenresViewSet)
router.register(
    'titles',
    views.TitlesViewSet,
    basename=Titles
)

urlpatterns = [
    path('v1/', include(router.urls)),
]
