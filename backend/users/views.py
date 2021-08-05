from django.db.models import Case, When

from djoser.views import UserViewSet

from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.pagination import SizedPageNumberPagination
from .serializers import SubscriptionSerializer, UserRecipesSerializer


class CustomUserViewSet(UserViewSet):
    pagination_class = SizedPageNumberPagination

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if not user.is_authenticated:
            return queryset
        queryset = queryset.annotate(
            is_subscribed=Case(
                When(pk__in=user.subscriptions.values('pk'), then=True),
                default=False,
            ),
        )
        if self.action == 'subscriptions':
            queryset = queryset.prefetch_related('recipes')
        return queryset

    def get_serializer_class(self):
        if self.action == 'subscriptions':
            return UserRecipesSerializer
        if self.action == 'subscribe':
            return SubscriptionSerializer
        return super().get_serializer_class()

    @action(methods=['get'],
            detail=False,
            permission_classes=[permissions.IsAuthenticated])
    def subscriptions(self, request, *args, **kwargs):
        queryset = self.filter_queryset(
            self.get_queryset()
        ).filter(is_subscribed=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'],
            detail=True,
            permission_classes=[permissions.IsAuthenticated])
    def subscribe(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data={'to_user': instance.pk})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=UserRecipesSerializer(instance).data,
            status=status.HTTP_201_CREATED,
        )

    @subscribe.mapping.delete
    def unsubscribe(self, request, *args, **kwargs):
        request.user.subscriptions.remove(self.get_object())
        return Response(status=status.HTTP_204_NO_CONTENT)
