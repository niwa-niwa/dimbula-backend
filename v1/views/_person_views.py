from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from person.models import Person
from v1.serializers import PersonSerializer


# not need
# class PersonViewSet(viewsets.ModelViewSet):
#     queryset = Person.objects.all()
#     serializer_class = PersonSerializer

class PersonView(APIView):
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
