from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()

app_name = 'v1'

urlpatterns = [
    path('', include(router.urls)),
    path('persons/', PersonView.as_view(), name='person_list'),
    path('persons/create/', PersonView.as_view(), name='person_create'),

    path('task-folders/', TaskFolderView.as_view(), name='task-folder_list'),
    path('task-folders/create/', TaskFolderView.as_view(), name='task-folder_create'),
    path('task-folders/edit/<pk>/', TaskFolderView.as_view(), name='task-folder_edit'),
    path('task-folders/delete/<pk>/', TaskFolderView.as_view(), name='task-folder_delete'),

    path('task-sections/', TaskSectionView.as_view(), name='task-section_list'),
    path('task-sections/create/', TaskSectionView.as_view(), name='task-section_create'),
    path('task-sections/edit/<pk>/', TaskSectionView.as_view(), name='task-folder_edit'),
    path('task-sections/delete/<pk>/', TaskSectionView.as_view(), name='task-folder_delete'),


]
