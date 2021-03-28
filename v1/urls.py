from django.urls import path, include
from rest_framework import routers

from .views import *


router = routers.DefaultRouter()

app_name = 'v1'

urlpatterns = [
    path('', include(router.urls)),
    path('persons/', PersonView.as_view(), name='person_list'),
    path('persons/create/', PersonView.as_view(), name='person_create'),
    path('persons/edit/<pk>/', PersonView.as_view(), name='person_edit'),
    path('persons/delete/<pk>/', PersonView.as_view(), name='person_delete'),

    path('admin/', AdminView.as_view(), name="admin_person_list"),
    path('admin/create/', AdminView.as_view(), name="admin_person_create"),
    path('admin/edit/<pk>/', AdminView.as_view(), name="admin_person_edit"),
    path('admin/delete/<pk>/', AdminView.as_view(), name="admin_person_delete"),

    path('task-folders/', TaskFolderView.as_view(), name='task-folder_list'),
    path('task-folders/create/', TaskFolderView.as_view(), name='task-folder_create'),
    path('task-folders/edit/<pk>/', TaskFolderView.as_view(), name='task-folder_edit'),
    path('task-folders/delete/<pk>/', TaskFolderView.as_view(), name='task-folder_delete'),

    path('task-sections/', TaskSectionView.as_view(), name='task-section_list'),
    path('task-sections/create/', TaskSectionView.as_view(), name='task-section_create'),
    path('task-sections/edit/<pk>/', TaskSectionView.as_view(), name='task-folder_edit'),
    path('task-sections/delete/<pk>/', TaskSectionView.as_view(), name='task-folder_delete'),

    path('tasks/', TaskView.as_view(), name="task_list"),
    path('tasks/create/', TaskView.as_view(), name="task_create"),
    path('tasks/edit/<pk>/', TaskView.as_view(), name="task_edit"),
    path('tasks/delete/<pk>/', TaskView.as_view(), name="task_delete"),

    path('sub-tasks/', SubTaskView.as_view(), name="sub-task_list"),
    path('sub-tasks/create/', SubTaskView.as_view(), name="sub-task_create"),
    path('sub-tasks/edit/<pk>/', SubTaskView.as_view(), name="sub-task_edit"),
    path('sub-tasks/delete/<pk>/', SubTaskView.as_view(), name="sub-task_delete"),

]
