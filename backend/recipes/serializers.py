from djoser.conf import settings as djoser_settings

from rest_framework import serializers, validators
from rest_framework.exceptions import APIException

from .fields import Base64ImageField
from .models import (
    FavoriteRecipe,
    Ingredient,
    Recipe,
    RecipeIngredient,
    ShoppingCart,
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
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')

    def validate(self, attrs):
        amount = attrs['amount']
        if amount < 0:
            raise APIException('Количество не может быть меньше нуля')
        return attrs


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = RecipeIngredientSerializer(
        source='recipeingredient_set',
        many=True,
    )
    tags = TagSerializer(many=True)
    author = djoser_settings.SERIALIZERS.user(read_only=True)
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)

    class Meta:
        model = Recipe
        exclude = ('favorited_by', 'shopped_by')


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

    def validate(self, attrs):
        ingredients = [obj['id'] for obj in attrs['recipeingredient_set']]
        if len(ingredients) > len(set(ingredients)):
            raise serializers.ValidationError(
                'Пожалуйста, уберите дублирующиеся ингредиенты.'
            )
        return attrs

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

    class Meta:
        model = FavoriteRecipe
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                FavoriteRecipe.objects.all(),
                fields=('user', 'recipe'),
                message='recipe already in favorites',
            )
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True,
    )

    class Meta:
        model = ShoppingCart
        fields = '__all__'
        validators = [
            validators.UniqueTogetherValidator(
                ShoppingCart.objects.all(),
                fields=('user', 'recipe'),
                message='recipe already in shopping cart',
            )
        ]


class BaseRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
