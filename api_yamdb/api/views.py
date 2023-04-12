from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from . import permissions
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
            return Response(request.data, status=status.HTTP_200_OK)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        """After creation generate confirmation code and send by mail."""
        serializer.save()
        username = serializer.data.get('username')
        user = get_object_or_404(User, username=username)
        utils.send_email_with_confirmation_code(user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers)


@api_view(['POST'])
@csrf_exempt
def receive_token(request):
    """Receive token."""
    serializer = serializers.TokenObtainSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=serializer.data.get('username'))
    token = RefreshToken.for_user(user)
    token_serializer = serializers.TokenSerializer(
        data={'token': str(token.access_token)}
    )
    token_serializer.is_valid()
    return Response(token_serializer.data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Viewset for User."""
    serializer_class = serializers.UsersSerializer
    permission_classes = [IsAuthenticated & permissions.IsAdminPermission]
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'username'


class PersonalInformationView(RetrieveUpdateAPIView):
    serializer_class = serializers.UsersSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.UsersSerializer
        return serializers.UserProfileSerializer
