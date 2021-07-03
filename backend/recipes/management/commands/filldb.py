from random import sample

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from recipes.factories import FavoriteRecipeFactory, RecipeWithIngredientsFactory
from recipes.models import Recipe
from users.factories import UserFactory

User = get_user_model()

USERS = 10
RECIPES_PER_USER = 5
FAVORITES_PER_USER = 10


class Command(BaseCommand):
    help = 'Fills the DB with sample data'

    def handle(self, *args, **options):
        user_count = recipe_count = favorite_count = 0
        for user in range(USERS):
            author = UserFactory()
            user_count += 1
            for recipe in range(RECIPES_PER_USER):
                RecipeWithIngredientsFactory(author=author)
                recipe_count += 1
        users = User.objects.all()
        recipes = tuple(Recipe.objects.all())
        for user in users:
            to_favorites = sample(recipes, FAVORITES_PER_USER)
            for recipe in to_favorites:
                FavoriteRecipeFactory(user=user, recipe=recipe)
                favorite_count += 1
        self.stdout.write(
            f'Added {user_count} users, {recipe_count} recipes'
            f' and {favorite_count} favorites'
        )
