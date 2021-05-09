from datetime import date
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from person.models import Person
from v1.serializers.task_serializers import *


class InboxView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        tasks = Task.objects.filter(person=request.user.id, taskFolder__isnull=True )
        serializer = TaskDetailSerializer(tasks, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class TodayView(APIView):
    permission_classes = [permissions.IsAuthenticated]  
    def get(self, request):
        tasks = Task.objects.filter(person=request.user.id, due_date__date=date.today() )
        serializer = TaskDetailSerializer(tasks, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class StarsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        tasks = Task.objects.filter(person=request.user.id, is_star=True )
        serializer = TaskDetailSerializer(tasks, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class AllTasksView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        tasks = Task.objects.filter(person=request.user.id)
        serializer = TaskDetailSerializer(tasks, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class TaskFolderDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        task_folder = get_object_or_404(TaskFolder, pk=pk, person=request.user.id)
        serializer = TaskFolderDetailSerializer(instance=task_folder)
        return Response(serializer.data, status.HTTP_200_OK)


class TaskFolderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):

        serializer = TaskFolderSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
        )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    def get(self, request):
        person = get_object_or_404(Person, pk=request.user.id)

        task_folders = TaskFolder.objects.filter(person=person)

        serializer = TaskFolderSerializer(task_folders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        person = get_object_or_404(Person, pk=request.user.id)

        task_folder = get_object_or_404(TaskFolder, pk=pk, person=person)

        serializer = TaskFolderSerializer(instance=task_folder, data=request.data)

        if serializer.is_valid(raise_exception=True) :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


    def delete(self, request, pk):

        task_folder = get_object_or_404(TaskFolder, pk=pk, person=request.user.id)

        task_folder.delete()
        
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskSectionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TaskSectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    
    def get(self, request):
        task_sections = TaskSection.objects.filter(person=request.user.id)
        serializer = TaskSectionSerializer(task_sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def patch(self, request, pk):
        task_section = get_object_or_404(TaskSection, pk=pk, person=request.user.id)
        serializer = TaskSectionSerializer(instance=task_section, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        task_section = get_object_or_404(TaskSection, pk=pk, person=request.user.id)
        task_section.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        serializer = TaskDetailSerializer(instance=task)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        tasks = Task.objects.filter(person=request.user.id)
        serializer = TaskSerializer(instance=tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def patch(self, request, pk):
        task = get_object_or_404(Task, pk=pk, person=request.user.id)
        serializer = TaskSerializer(instance=task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    def delete(self, request, pk):
        task = get_object_or_404(Task, pk=pk, person=request.user.id)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SubTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request):
        sub_tasks = SubTask.objects.filter(person=request.user.id)
        serializer = SubTaskSerializer(instance=sub_tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        sub_task = get_object_or_404(SubTask, pk=pk, person=request.user.id)
        serializer = SubTaskSerializer(instance=sub_task, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        sub_task = get_object_or_404(SubTask, pk=pk, person=request.user.id)
        sub_task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
