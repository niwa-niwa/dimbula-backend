from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.response import Response

from task.models import Task
from v1.serializers._task_serializers import *

class TaskFolderView(APIView):
    serializer_class = TaskFolderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request):
        return Response(status=status.HTTP_201_CREATED)

    def patch(self, request):
        return Response(status=status.HTTP_200_OK)

    def delete(self, request):
        return Response(status=status.HTTP_200_OK)