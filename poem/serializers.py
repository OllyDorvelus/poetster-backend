from rest_framework import serializers

from django.utils.timesince import timesince

from poem.models import Poem, Genre, Category

from user.serializers import UserSerializer

class GenreSerializer(serializers.ModelSerializer):
    """Serializer for genre - all methods"""
    class Meta:
        model = Genre
        fields = ('id', 'name', 'disabled', 'created', 'updated')
        read_only_fields = ('id', 'created', 'updated')


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category - all methods"""
    class Meta:
        model = Category
        fields = ('id', 'name', 'disabled')
        read_only_fields = ('id',)

class SimpleGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')

class PoemSerializer(serializers.ModelSerializer):
    """Serializer for creating a poem"""
    genre = serializers.SlugRelatedField(queryset=Genre.objects.all(), slug_field='name')
    user = UserSerializer(read_only=True)
    categories = serializers.SlugRelatedField(queryset=Category.objects.all(), slug_field='name', many=True)
    timesince = serializers.SerializerMethodField()

    class Meta:
        model = Poem
        fields = ('id',
                  'user',
                  'title',
                  'summary',
                  'content',
                  'is_published',
                  'genre',
                  'categories',
                  'poem_count',
                  'timesince',
                  'created')

        read_only_fields = ('created', )

    def get_timesince(self, obj):
        return f'{timesince(obj.created)} ago'


class PoemImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading image to poem"""

    class Meta:
        model = Poem
        fields = ('id', 'image')
        read_only_fields = ('id',)

