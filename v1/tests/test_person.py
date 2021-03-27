from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from person.models import Person
from v1.serializers import PersonSerializer

from ._fake_data import *

PERSON_URL = '/api/v1/persons/'


class TestPerson(APITestCase):

    print("Start Person Test !!")
    
    def setUp(self):
        self.person = create_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=self.person)

    def test_getUser(self):
        excute_persons()
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

        self.assertTrue(response.data["id"])
        self.assertEqual(response.data["name"], new_user["name"])
        self.assertEqual(response.data["email"], new_user["email"])
