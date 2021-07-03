import factory
from factory import fuzzy

from users.factories import UserFactory
from .models import FavoriteRecipe, Ingredient, Recipe, RecipeIngredient


class RecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Recipe

    name = factory.Faker('text', max_nb_chars=20)
    author = factory.SubFactory(UserFactory)
    cooking_time = fuzzy.FuzzyInteger(5, 120, 5)
    text = factory.Faker('paragraph')


class RecipeIngredientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RecipeIngredient

    amount = fuzzy.FuzzyInteger(5, 200, 5)
    ingredient = fuzzy.FuzzyChoice(Ingredient.objects.all())


class RecipeWithIngredientsFactory(RecipeFactory):
    ingredient_1 = factory.RelatedFactory(RecipeIngredientFactory, 'recipe')
    ingredient_2 = factory.RelatedFactory(RecipeIngredientFactory, 'recipe')
    ingredient_3 = factory.RelatedFactory(RecipeIngredientFactory, 'recipe')
    ingredient_4 = factory.RelatedFactory(RecipeIngredientFactory, 'recipe')
    ingredient_5 = factory.RelatedFactory(RecipeIngredientFactory, 'recipe')


class FavoriteRecipeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FavoriteRecipe

    user = factory.SubFactory(UserFactory)
    recipe = factory.SubFactory(RecipeFactory)
