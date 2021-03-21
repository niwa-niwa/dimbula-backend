from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()
# router.register('users', views.UserViewSet) # not need

app_name = 'v1'

urlpatterns = [
    path('', include(router.urls)),
    path('persons/', PersonView.as_view(), name='person_list'),
    path('persons/create/', PersonView.as_view(), name='person_create'),

    path('taskfolders/', TaskFolderView.as_view(), name='taskfolder_list'),
    path('taskfolders/create/', TaskFolderView.as_view(), name='taskfolder_create'),
    path('taskfolders/edit/', TaskFolderView.as_view(), name='taskfolder_edit'),
    path('taskfolders/delete/', TaskFolderView.as_view(), name='taskfolder_delete'),

]
