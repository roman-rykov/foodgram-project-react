from django.conf.urls import url
from django.urls import include

from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

recipes_router = routers.DefaultRouter()
recipes_router.register(r'tags', TagViewSet)
recipes_router.register(r'ingredients', IngredientViewSet)
recipes_router.register(r'recipes', RecipeViewSet)

app_name = 'recipes'

urlpatterns = [
    url(r'^', include(recipes_router.urls)),
]
