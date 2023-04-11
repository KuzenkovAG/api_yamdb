from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt

from . import serializers
from . import utils

User = get_user_model()


class SignUpUser(CreateAPIView):
    """Create new user, if user exist - sent confirmation_code to email."""
    serializer_class = serializers.UserCreateSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        user = User.objects.filter(username=username, email=email)
        if user.exists() and user[0].email == email:
            utils.send_email_with_confirmation_code(user[0])
            return Response(request.data, status=status.HTTP_201_CREATED)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()
        username = serializer.data.get('username')
        user = get_object_or_404(User, username=username)
        utils.send_email_with_confirmation_code(user)


@api_view(['POST'])
@csrf_exempt
def receive_token(request):
    serializer = serializers.TokenObtainSerializer(data=request.data)
    serializer.is_valid()
    user = get_object_or_404(User, username=serializer.data.get('username'))
    token = RefreshToken.for_user(user)
    token_serializer = serializers.TokenSerializer(
        data={'token': str(token.access_token)}
    )
    token_serializer.is_valid()
    return Response(token_serializer.data, status=status.HTTP_200_OK)
