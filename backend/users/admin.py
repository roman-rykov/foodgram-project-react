from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count

from .models import CustomUser, Subscription


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'subscriptions_count', 'subscribers_count',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request).annotate(
            Count('subscriptions'), Count('subscribers'),
        )
        return queryset

    def subscriptions_count(self, obj):
        return obj.subscriptions__count

    def subscribers_count(self, obj):
        return obj.subscribers__count

    subscriptions_count.short_description = 'подписок'
    subscribers_count.short_description = 'подписчиков'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user')
    search_fields = (
        'from_user__username', 'from_user__email',
        'to_user__username', 'to_user__email',
    )
