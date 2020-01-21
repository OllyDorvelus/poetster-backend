import django_filters

from poem.models import Poem, Genre, Category


class PoemFilter(django_filters.FilterSet):
    """Custom filter set for poem model"""
    user = django_filters.CharFilter(field_name='user__name', lookup_expr='iexact')
    genre = django_filters.CharFilter(field_name='genre__name', lookup_expr='iexact')
    category = django_filters.CharFilter(field_name='categories__name', lookup_expr='iexact')

    class Meta:
        model = Poem
        fields = ['user', 'genre', 'category']


class GenreFilter(django_filters.FilterSet):
    """Custom filter set for genre model"""
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')

    class Meta:
        model = Genre
        fields = ['name']


class CategoryFilter(django_filters.FilterSet):
    """Custom filter set for category model"""
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')

    class Meta:
        model = Category
        fields = ['name']

