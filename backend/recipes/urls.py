from django.conf.urls import url
from django.urls import include

from rest_framework import routers

from .views import TagViewSet

recipes_router = routers.DefaultRouter()
recipes_router.register(r'tags', TagViewSet)

app_name = 'recipes'

urlpatterns = [
    url(r'^', include(recipes_router.urls)),
]
