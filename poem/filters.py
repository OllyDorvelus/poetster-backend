from django.contrib.auth import get_user_model

import django_filters

from poem.models import Poem, Genre, Category

User = get_user_model()


class PoemFilter(django_filters.FilterSet):
    """Custom filter set for poem model"""
    user = django_filters.ModelChoiceFilter(field_name='user__pen_name', to_field_name='pen_name',
                                            queryset=User.objects.all())
    genre = django_filters.ModelMultipleChoiceFilter(field_name='genre__name', to_field_name='name',
                                                     queryset=Genre.objects.active())
    category = django_filters.ModelMultipleChoiceFilter(field_name='categories__name', to_field_name='name',
                                                        queryset=Category.objects.active())

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
