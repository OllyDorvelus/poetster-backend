from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions

from poem.serializers import GenreSerializer, CategorySerializer
from poem.models import Genre, Category


class GenreViewSet(viewsets.ModelViewSet):
    """Handle creating, updating, deleting genres, admin only"""
    serializer_class = GenreSerializer
    queryset = Genre.objects.active()


class CategoryViewSet(viewsets.ModelViewSet):
    """Handle creating, updating, deleting categories, admin only"""
    serializer_class = CategorySerializer
    queryset = Category.objects.active()
