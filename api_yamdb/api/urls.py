from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenVerifyView

from . import views

router = SimpleRouter()
router.register(r'users', views.UserViewSet, basename='Users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews', views.ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet,
    basename='comments'
)


urlpatterns = [
    path('v1/auth/signup/', views.create_user, name='sign_up'),
    path('v1/auth/token/', views.receive_token, name='token_obrain'),
    path('v1/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path(
        'v1/users/me/',
        views.PersonalInformationView.as_view(),
        name='personal'
    ),
    path('v1/', include(router.urls)),
]
