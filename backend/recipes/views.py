from rest_framework import filters, viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly

from .models import Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]  # TODO: Fix permissions


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    filters.SearchFilter.search_param = 'name'
    search_fields = ['name']
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]  # TODO: Fix permissions
