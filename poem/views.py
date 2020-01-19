from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework import generics

from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


from user.permissions import AdminWrite, OwnerPermission

from poem.serializers import GenreSerializer, CategorySerializer, PoemCreateSerializer, PoemSerializer
from poem.models import Genre, Category, Poem
from poem.filters import PoemFilter

from poem.pagination import StandardResultsSetPagination


class GenreViewSet(viewsets.ModelViewSet):
    """Handle creating, updating, deleting genres, admin only"""
    serializer_class = GenreSerializer
    permission_classes = (AdminWrite,)
    queryset = Genre.objects.all()

    def list(self, request, *args, **kwargs):
        """Retrieve only enabled genres"""
        self.queryset = Genre.objects.active()
        return super().list(request, *args, **kwargs)


class CategoryViewSet(viewsets.ModelViewSet):
    """Handle creating, updating, deleting categories, admin only"""
    serializer_class = CategorySerializer
    permission_classes = (AdminWrite,)
    queryset = Category.objects.all()

    def list(self, request, *args, **kwargs):
        """Retrieve only enabled categories"""
        self.queryset = Category.objects.active()
        return super().list(request, *args, **kwargs)


class CreatePoemView(generics.ListCreateAPIView):
    """Handle creation of poems and listing of poems
    POST [title, summary, content, is_published, categories]
    """
    serializer_class = PoemCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Poem.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['title']
    search_fields = ['title', 'user__name']
    filterset_class = PoemFilter
    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PoemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PoemSerializer
    queryset = Poem.objects.all()
    permission_classes = [OwnerPermission]
