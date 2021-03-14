from django.urls import path, include
from rest_framework import routers, urlpatterns

from . import views


router = routers.DefaultRouter()
router.register('users', views.UserViewSet)

app_name = 'v1'

urlpatterns = [
    path('', include(router.urls)),
]
