from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics

from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


from user.permissions import OwnerPermission, IsAdminOrReadOnly

from poem.serializers import GenreSerializer, CategorySerializer, PoemSerializer
from poem.models import Genre, Category, Poem
from poem.filters import PoemFilter, GenreFilter, CategoryFilter

from poem.pagination import StandardResultsSetPagination


class GenreViewSet(viewsets.ModelViewSet):
    """Handle creating, updating, deleting genres, admin only"""
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Genre.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['name']
    search_fields = ['name']
    filterset_class = GenreFilter

    def list(self, request, *args, **kwargs):
        """Retrieve only enabled genres"""
        self.queryset = Genre.objects.active().order_by('name')
        return super().list(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    """Handle creating, updating, deleting categories, admin only"""
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Category.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['name']
    search_fields = ['name']
    filterset_class = CategoryFilter

    def list(self, request, *args, **kwargs):
        """Retrieve only enabled categories"""
        self.queryset = Category.objects.active().order_by('name')
        return super().list(request, *args, **kwargs)


class PoemViewSet(viewsets.ModelViewSet):
    """Handle creation of poems and listing of poems
    POST [title, summary, content, is_published, categories]
    """
    serializer_class = PoemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, OwnerPermission]
    queryset = Poem.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['title', 'created']
    search_fields = ['title', 'user__name']
    filterset_class = PoemFilter
    pagination_class = StandardResultsSetPagination


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

