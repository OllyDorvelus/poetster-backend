from django.shortcuts import get_object_or_404

from rest_framework import generics, authentication, permissions
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework.response import Response

from user.serializers import UserSerializer, UserCreateSerializer, AuthTokenSerializer

from user.models import Profile

class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserCreateSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManagaeUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return auththenticated user"""
        return self.request.user


class SubscribeUserToggleView(APIView):
    """Subscribe/Unsubscribe the user"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        user_profile = get_object_or_404(Profile, pk=pk)
        message = 'Not allowed'
        if request.user.is_authenticated:
            is_subscribed = Profile.objects.like_toggle(request.user.profile, user_profile)
            return Profile({'subscribed': is_subscribed})
        return Response({'message': message}, status=status.HTTP_401_UNAUTHORIZED)
