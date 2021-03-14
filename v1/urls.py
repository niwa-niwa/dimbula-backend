from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
# router.register('users', views.UserViewSet) # not need

app_name = 'v1'

urlpatterns = [
    path('', include(router.urls)),
    path('users', views.UserView.as_view(), name='user_list'),
    path('users/create', views.UserView.as_view(), name='user_create'),
]
