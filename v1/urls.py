from django.urls import path, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
# router.register('users', views.UserViewSet) # not need

app_name = 'v1'

urlpatterns = [
    path('', include(router.urls)),
    path('persons/', views.PersonView.as_view(), name='person_list'),
    path('persons/create/', views.PersonView.as_view(), name='person_create'),
]
