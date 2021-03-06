from collections import Counter

from django.db.models import Case, Prefetch, When
from django.http.response import HttpResponse

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .models import (
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag,
    User,
)
from .pagination import SizedPageNumberPagination
from .permissions import IsAdmin, IsAuthenticated, IsAuthor, ReadOnly
from .serializers import (
    BaseRecipeSerializer,
    FavoriteRecipeSerializer,
    IngredientSerializer,
    RecipeCUDSerializer,
    RecipeSerializer,
    ShoppingCartSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [ReadOnly | IsAdmin]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientFilter
    permission_classes = [ReadOnly | IsAdmin]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.prefetch_related(
        'tags',
        Prefetch(
            'recipeingredient_set',
            queryset=RecipeIngredient.objects.select_related('ingredient'),
        ),
    ).all()
    permission_classes = [ReadOnly | IsAuthor | IsAuthenticated | IsAdmin]
    pagination_class = SizedPageNumberPagination
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
                is_favorited=Case(  # Fetch favorite status
                    When(
                        pk__in=user.favorite_recipes.values('pk'),
                        then=True,
                    ),
                    default=False,
                ),
                is_in_shopping_cart=Case(  # Fetch shopping cart status
                    When(
                        pk__in=user.shopping_cart.values('pk'),
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
        if self.action == 'shopping_cart':
            return ShoppingCartSerializer
        if self.request.method not in permissions.SAFE_METHODS:
            return RecipeCUDSerializer
        return RecipeSerializer

    def add_recipe_relation(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data={'recipe': instance.pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=BaseRecipeSerializer(instance).data,
            status=status.HTTP_201_CREATED,
        )

    @action(methods=['get'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, *args, **kwargs):
        return self.add_recipe_relation(request, *args, **kwargs)

    @favorite.mapping.delete
    def remove_from_favorites(self, request, *args, **kwargs):
        request.user.favorite_recipes.remove(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def shopping_cart(self, request, *args, **kwargs):
        return self.add_recipe_relation(request, *args, **kwargs)

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, *args, **kwargs):
        request.user.shopping_cart.remove(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'],
            detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, reqeust, *args, **kwargs):
        queryset = self.get_queryset().filter(is_in_shopping_cart=True)
        shopping_list, units = Counter(), dict()
        for recipe in queryset:
            for obj in recipe.recipeingredient_set.all():
                shopping_list[obj.ingredient.name] += obj.amount
                units[obj.ingredient.name] = obj.ingredient.measurement_unit
        text = '?????? ???????????? ??????????????:\n'
        for ingredient, amount in shopping_list.items():
            text += f'{ingredient} {amount} {units[ingredient]}\n'
        return HttpResponse(text, content_type='text/plain')
