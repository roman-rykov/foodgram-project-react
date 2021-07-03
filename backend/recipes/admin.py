from django.contrib import admin

from .forms import TagAdminForm
from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')
    search_fields = ('name', 'slug')
    form = TagAdminForm
    prepopulated_fields = {'slug': ('name', )}
