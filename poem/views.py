from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend

from user.permissions import OwnerPermission, IsAdminOrReadOnly

from poem.serializers import GenreSerializer, CategorySerializer, PoemSerializer, PoemImageSerializer
from poem.models import Genre, Category, Poem
from poem.filters import PoemFilter, GenreFilter, CategoryFilter

from poem.pagination import StandardResultsSetPagination
from poem.tasks import add
from poem.tasks import process_image_file

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
        add.delay(2,3)
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


    def get_serializer_class(self):
        if self.action == 'upload_image':
            self.serializer_class = PoemImageSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload image for a poem"""
        poem = self.get_object()
        serializer = self.get_serializer(
            poem,
            data=request.data
        )

        if serializer.is_valid():
            instance = serializer.save()
            instance_id = instance.id
            process_image_file.delay(instance_id, (50,50))
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(methods=['GET'], detail=True, url_path='up-vote')
    def up_vote(self, request, pk=None):
        poem = self.get_object()
        message = "Not allowed"
        if request.user.is_authenticated:
            is_upvoted = Poem.objects.up_vote_toggle(request.user, poem)
            return Response({'up_voted': is_upvoted})
        return Response({"message": message}, status=status.HTTP_401_UNAUTHORIZED)


class UpVotePoemToggleView(APIView):
    """Subscribe/Unsubscribe the user"""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, pk):
        poem = get_object_or_404(Poem, pk=pk)
        message = "Not allowed"
        if request.user.is_authenticated():
            is_upvoted = Poem.objects.up_vote_toggle(request.user, poem)
            return Poem({'up_voted': is_upvoted})
        return Response({"message": message}, status=400)