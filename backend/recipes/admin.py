from django.contrib import admin

from .forms import TagAdminForm
from .models import FavoriteRecipe, Ingredient, Recipe, RecipeIngredient, Tag


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ('ingredient', )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    form = TagAdminForm
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ('name', )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorited_count')
    list_filter = ('tags', )
    search_fields = ('name', 'author__username')
    inlines = (RecipeIngredientInline, )

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('favorited_by')


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')
    search_fields = ('user__username', 'user__email', 'recipe__name')
