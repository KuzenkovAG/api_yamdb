from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView

from . import views

urlpatterns = [
    path('v1/auth/signup/', views.SignUpUser.as_view(), name='sign_up'),
    path('v1/auth/token/', views.receive_token, name='token_obrain'),
    path('v1/auth/verify/', TokenVerifyView.as_view(), name='token_verify')
]

