from rest_framework import serializers

from poem.models import Poem, Genre, Category


class GenreSerializer(serializers.ModelSerializer):
    """Serializer for genre - all methods"""
    class Meta:
        model = Genre
        fields = ('id', 'name', 'disabled', 'created', 'updated')


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for category - all methods"""
    class Meta:
        model = Category
        fields = ('id', 'name', 'disabled')


class PoemSerializer(serializers.ModelSerializer):
    """Serializer for creating a poem"""

    class Meta:
        model = Poem
        fields = ('id', 'title', 'summary', 'content', 'is_published', 'genre', 'categories')

