# filters.py

import django_filters
from django.contrib.auth.models import User

class UserFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')

    class Meta:
        model = User
        fields = []

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            username__icontains=value
        ) | queryset.filter(
            email__icontains=value
        )
