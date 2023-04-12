import json

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

# from . import permissions
from . import serializers
from . import utils

User = get_user_model()


@api_view(['POST'])
def create_user(request):
    """User creation and send confirmation code by mail."""
    username = request.data.get('username')
    email = request.data.get('email')
    user = User.objects.filter(username=username, email=email)
    if user.exists() and user[0].email == email:
        utils.send_email_with_confirmation_code(user[0])
        return Response(request.data, status=status.HTTP_200_OK)
    serializer = serializers.UserCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        utils.send_email_with_confirmation_code(user[0])
        return Response(request.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@csrf_exempt
def receive_token(request):
    """Receive token."""
    serializer = serializers.TokenObtainSerializer(data=request.data)
    if serializer.is_valid():
        user = get_object_or_404(User, username=request.data.get('username'))
        token = RefreshToken.for_user(user)
        json_data = json.dumps({'token': str(token.access_token)})
        return Response(json_data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """Viewset for User."""
    serializer_class = serializers.UsersSerializer
    # permission_classes = [IsAuthenticated & permissions.IsAdminPermission]
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    lookup_field = 'username'


class PersonalInformationView(RetrieveUpdateAPIView):
    """Update personal information of User."""
    serializer_class = serializers.UsersSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(User, id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.UsersSerializer
        return serializers.UserProfileSerializer
