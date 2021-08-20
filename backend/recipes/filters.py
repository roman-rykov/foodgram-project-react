import re

import django_filters
from django_filters import rest_framework

from .models import Tag


def individual_words_startswith(queryset, field, value):
    lookup = '__'.join([field, 'iregex'])
    queryset = queryset.filter(**{lookup: r'\m' + re.escape(value)})
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
    is_in_shopping_cart = django_filters.BooleanFilter(
        label='Is in shopping cart',
    )


class IngredientFilter(rest_framework.FilterSet):
    name = django_filters.CharFilter(method=individual_words_startswith)
