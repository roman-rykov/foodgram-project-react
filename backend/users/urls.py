from django.conf.urls import url
from django.urls import include

from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('users', views.CustomUserViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^auth/', include('djoser.urls.authtoken')),
    url(r'^', include('djoser.urls')),
]
