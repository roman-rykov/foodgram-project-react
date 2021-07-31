from django.db.models import Case, When

from djoser.views import UserViewSet

from rest_framework import pagination, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response


class CustomUserViewSet(UserViewSet):
    pagination_class = pagination.PageNumberPagination

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if not user.is_authenticated:
            return queryset
        queryset = queryset.annotate(
            is_subscribed=Case(
                When(pk__in=user.subscriptions.all(), then=True),
                default=False,
            ),
        )
        return queryset

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
        obj = self.get_object()
        request.user.subscriptions.add(obj)
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, *args, **kwargs):
        obj = self.get_object()
        request.user.subscriptions.remove(obj)
        return Response(status=status.HTTP_204_NO_CONTENT)
