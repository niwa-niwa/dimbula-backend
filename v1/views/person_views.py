from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from person.models import Person
from v1.serializers import PersonSerializer


class PersonView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        person = Person.objects.get(id=request.user.id)
        serializer = PersonSerializer(person)
        return Response(serializer.data)


    def patch(self, request, pk):
        person = get_object_or_404(Person, id=request.user.id)
        serializer = PersonSerializer(instance=person, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request, pk):
        person = get_object_or_404(Person, id=request.user.id)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminView(APIView):
    permission_classes=[permissions.IsAdminUser]

    def get(self, request):
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response(serializer.data)
    

    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status = status.HTTP_201_CREATED)


    def patch(self, request, pk):
        person = get_object_or_404(Person, pk=pk)
        serializer = PersonSerializer(instance=person, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        person = get_object_or_404(Person, pk=pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)