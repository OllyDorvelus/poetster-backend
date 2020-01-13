import django_filters

from poem.models import Poem


class PoemFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(field_name='user__name', lookup_expr='iexact')
    genre = django_filters.CharFilter(field_name='genre__name', lookup_expr='iexact')
    category = django_filters.CharFilter(field_name='categories__name', lookup_expr='iexact')

    class Meta:
        model = Poem
        fields = ['genre']

