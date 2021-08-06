from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Subscription


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'subscriptions_count', 'subscribers_count',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related(
            'subscriptions', 'subscribers',
        )
        return queryset


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user')
    search_fields = (
        'from_user__username', 'from_user__email',
        'to_user__username', 'to_user__email',
    )
