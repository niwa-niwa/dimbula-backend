from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from person.models import Person
from v1.serializers import PersonSerializer

from .fake_data import *

ENDPOINT = '/api/v1/persons/'


class TestPerson(APITestCase):
    print("Start Person Test !!")


    def setUp(self):
        create_taskData()
        self.person = create_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=self.person)


    def test_getUser(self):
        responce = self.client.get(ENDPOINT)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

        person = Person.objects.get(id=self.person.id)
        serializer = PersonSerializer(person)
        self.assertEqual(responce.data, serializer.data)


    def test_patch_user(self):
        payload={"name":"michel"}
        response = self.client.patch(ENDPOINT + "edit/" + str(self.person.id) + "/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        person = Person.objects.get(id=self.person.id)
        self.assertEqual(response.data["name"], person.name)


    def test_delete_user(self):
        response = self.client.delete(ENDPOINT + "delete/" + str(self.person.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        person_num = Person.objects.filter(id=self.person.id).count()
        self.assertEqual(person_num, 0)


class TestAdmin(APITestCase):
    print('Start Admin TEST !!')

    ENDPOINT = "/api/v1/admin/"

    def setUp(self):
        create_taskData()
        self.person = create_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=self.person)


    def test_admin_users_GET(self):
        response = self.client.get(self.ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        self.assertEqual(len(response.data), len(serializer.data))


    def test_createUser(self):
        new_user = {
            'firebase_id':"ThisIsId",
            'name':"TEST MAN",
            'email':"ccc@ccc.com",
            'provider_id':"facebook.com",
        }

        response = self.client.post(self.ENDPOINT + "create/", new_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = Person.objects.get(id=response.data["id"])
        self.assertEqual(user.name, new_user["name"])
        self.assertEqual(user.email, new_user["email"])


    def test_admin_edit_user_PATCH(self):
        person = create_person()
        payload = {"name":"edit_user"}
        response = self.client.patch(self.ENDPOINT + "edit/" + str(person.id) + "/", payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        person = Person.objects.get(id=person.id)
        self.assertEqual(person.name, payload["name"])


    def test_admin_delete_user_DELETE(self):
        person = create_person()
        response = self.client.delete(self.ENDPOINT + "delete/" + str(person.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        num = Person.objects.filter(id=person.id).count()
        self.assertEqual(num, 0)