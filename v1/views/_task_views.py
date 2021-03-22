from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from task.models import Task
from v1.serializers._task_serializers import *


class TaskFolderView(APIView):
    serializer_class = TaskFolderSerializer
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


    def patch(self, request):
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        return Response(status=status.HTTP_200_OK)
