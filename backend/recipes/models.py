from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='наименование',
        max_length=200,
    )
    color = models.CharField(
        verbose_name='цвет',
        max_length=7,
        default='#FFFFFF',
        validators=[RegexValidator('^#(?:[0-9a-fA-F]{1,2}){3}$')])
    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='наименование',
        max_length=200,
    )
    measurement_unit = models.CharField(
        verbose_name='еденица измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipe(models.Model):
    tags = models.ManyToManyField(
        to=Tag,
        related_name='recipes',
        verbose_name='теги',
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор',
    )
    name = models.CharField(
        verbose_name='название',
        max_length=200,
    )
    image = models.ImageField(
        verbose_name='изображение',
        blank=True,
    )
    text = models.TextField(
        verbose_name='текст',
    )
    ingredients = models.ManyToManyField(
        to=Ingredient,
        related_name='recipes',
        through='RecipeIngredient',
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='время приготовления',
    )
    favorited_by = models.ManyToManyField(
        to=User,
        related_name='favorite_recipes',
        through='FavoriteRecipe',
    )
    shopped_by = models.ManyToManyField(
        to=User,
        related_name='shopping_cart',
        through='ShoppingCart',
    )

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        to=Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )
    ingredient = models.ForeignKey(
        to=Ingredient,
        on_delete=models.RESTRICT,
        verbose_name='ингредиент',
    )
    amount = models.PositiveIntegerField(verbose_name='количество')

    class Meta:
        constraints = [models.constraints.UniqueConstraint(
            fields=('recipe', 'ingredient'),
            name='unique ingredients for each recipe',
        )]
        verbose_name = 'ингредиент в рецепте'
        verbose_name_plural = 'ингредиенты в рецептах'

    def __str__(self):
        return f'{self.amount} {self.ingredient} in {self.recipe}'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.constraints.UniqueConstraint(
            fields=('user', 'recipe'),
            name='the recipe is already in this user\'s favorites',
        )]


class ShoppingCart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(to=Recipe, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.constraints.UniqueConstraint(
            fields=('user', 'recipe'),
            name='the recipe is already in this user\'s shopping cart',
        )]
