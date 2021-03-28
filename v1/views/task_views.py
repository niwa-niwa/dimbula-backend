from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from v1.serializers.task_serializers import *


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

        task_folders = TaskFolder.objects.filter(person=request.user.id)

        serializer = TaskFolderSerializer(task_folders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


    def patch(self, request, pk):

        task_folder = get_object_or_404(TaskFolder, pk=pk, person=request.user.id)

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
        return Response(status=status.HTTP_201_CREATED)


    def get(self, request):
        return Response(status=status.HTTP_200_OK)


    def patch(self, request, pk):
        return Response(status=status.HTTP_200_OK)


    def delete(self, request, pk):
        return Response(status=status.HTTP_204_NO_CONTENT)
