from django.conf.urls import url
from django.contrib import admin
from django.urls import include

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^api/', include('recipes.urls')),
    url(r'^api/', include('users.urls')),
]
