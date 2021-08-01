from django.contrib.auth import get_user_model
from django.db.models import Case, Prefetch, When

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import pagination, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag,
)
from .serializers import (
    FavoriteRecipeSerializer,
    IngredientSerializer,
    RecipeCUDSerializer,
    RecipeSerializer,
    TagSerializer,
)

User = get_user_model()


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]  # TODO: Fix permissions


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]  # TODO: Fix permissions


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related(
        'tags',
        Prefetch(
            'recipeingredient_set',
            queryset=RecipeIngredient.objects.select_related('ingredient'),
        ),
    ).all()
    pagination_class = pagination.PageNumberPagination  # TODO: Create new pagination class
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if user.is_authenticated:  # Get personal data for authenticated user
            queryset = queryset.prefetch_related(
                Prefetch(  # Fetch recipe authors with subscription status
                    'author',
                    queryset=User.objects.annotate(
                        is_subscribed=Case(
                            When(pk__in=user.subscriptions.all(), then=True),
                            default=False,
                        ),
                    ),
                ),
            ).annotate(
                is_favorited=Case(  # Get favorite status
                    When(
                        pk__in=user.favorite_recipes.values('pk'),
                        then=True,
                    ),
                    default=False,
                ),
            )
        else:
            queryset = queryset.select_related('author')
        return queryset

    def get_serializer_class(self):
        if self.action == 'favorite':
            return FavoriteRecipeSerializer
        if self.request.method not in permissions.SAFE_METHODS:
            return RecipeCUDSerializer
        return RecipeSerializer

    @action(methods=['get'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, *args, **kwargs):
        data = {'recipe': self.get_object().pk}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_from_favorites(self, request, *args, **kwargs):
        self.get_object().favorited_by.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
