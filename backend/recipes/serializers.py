from djoser.conf import settings

from rest_framework import serializers, validators

from .fields import Base64ImageField
from .models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeIngredientCUDSerializer(RecipeIngredientSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=0)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set',
        many=True,
    )
    tags = TagSerializer(many=True)
    author = settings.SERIALIZERS.user(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True)

    class Meta:
        model = Recipe
        fields = '__all__'


class RecipeCUDSerializer(RecipeSerializer):
    ingredients = RecipeIngredientCUDSerializer(
        source='recipeingredient_set',
        many=True,
    )
    tags = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Tag.objects.all(),
        many=True,
    )
    image = Base64ImageField(help_text='base64-encoded image')
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def update_ingredients(self, recipe, ingredients_data):
        recipe.recipeingredient_set.all().delete()
        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            ) for ingredient in ingredients_data]
        )
        return recipe

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set')
        instance = super().create(validated_data)
        return self.update_ingredients(instance, ingredients_data)

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set')
        instance = self.update_ingredients(instance, ingredients_data)
        return super().update(instance, validated_data)


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True,
    )
    id = serializers.IntegerField(source='recipe.id', required=False)
    name = serializers.CharField(source='recipe.name', required=False)
    image = serializers.ImageField(source='recipe.image', required=False)
    cooking_time = serializers.IntegerField(
        source='recipe.cooking_time',
        required=False,
    )

    class Meta:
        model = FavoriteRecipe
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                FavoriteRecipe.objects.all(),
                fields=['user', 'recipe'],
                message='recipe already in favorites',
            )
        ]
