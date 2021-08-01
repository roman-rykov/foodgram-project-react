import re

import django_filters
from django_filters import rest_framework

from .models import Tag


def individual_words_startswith(queryset, field, value):
    lookup = '__'.join([field, 'iregex'])
    queryset = queryset.filter(**{lookup: r'\b' + re.escape(value)})  # works with SQLite at least
    return queryset


class RecipeFilter(rest_framework.FilterSet):
    author = django_filters.NumberFilter(
        field_name='author__id',
        lookup_expr='exact',
    )
    tags = django_filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        queryset=Tag.objects.all(),
        to_field_name='slug',
    )
    is_favorited = django_filters.BooleanFilter(label='Is favorited')


class IngredientFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(method=individual_words_startswith)
