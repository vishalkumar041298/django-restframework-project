import django_filters
from watchlist_app.models import WatchList, StreamPlatform
from django.db import models

class MovieFilter(django_filters.FilterSet):
    class Meta:
        model = WatchList
        fields = {
            'title': ['iexact', 'icontains'],
            'avg_rating': ['gte', 'lte', 'range'],
            'platform__name': ['iexact', 'icontains']
        }


class StreamPlatformFilter(django_filters.FilterSet):    
    search = django_filters.CharFilter(method='filter_search')
    ordering = django_filters.OrderingFilter(
        fields=(
            ('name', 'name'),
        )
    )
    
    class Meta:
        model = StreamPlatform
        fields = []
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(name__icontains=value) |
            models.Q(about__icontains=value)
        )
        