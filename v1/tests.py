from django.db import models
from django.test import TestCase
from rest_framework import response, serializers, status
from rest_framework.test import APITestCase
from person.models import Person
from .serializers import PersonSerializer

PERSON_URL = 'http://127.0.0.1:8000/api/v1/persons/'

# Create your tests here.
class PersonTest(APITestCase):


    def test_getUser(self):
        responce = self.client.get(PERSON_URL)
        person = Person.objects.all()
        serializer = PersonSerializer(person, many=True)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(responce.data, serializer.data)


    def test_createUser(self):
        new_user = {
            'firebase_id':"ThisIsId",
            'name':"TEST MAN",
            'email':"ccc@ccc.com",
            'provider_id':"facebook.com",
        }

        response = self.client.post(PERSON_URL + "create/", new_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        person = Person.objects.all().first()
        serializer = PersonSerializer(person)

        self.assertTrue(response.data["id"])
        self.assertEqual(response.data["name"], new_user["name"])
        self.assertEqual(response.data["email"], new_user["email"])
        self.assertEqual(response.data["provider_id"], new_user["provider_id"])
