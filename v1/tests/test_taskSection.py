from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from person.models import Person
from task.models import TaskSection
from v1.serializers._task_serializers import *

ENDPOINT = '/api/v1/task-sections/'



class TestTaskSection(APITestCase):
    print('Start Task Section TEST !!')


    def setUp(self):
        self.person = Person.objects.create(
            firebase_id="firebase_user_uid",
            name="test_name",
            email="test_email@adb.com",
            email_verified=True,
            provider_id="google.com"
            )
        self.client = APIClient()
        self.client.force_authenticate(user=self.person)


    def test_create_testTaskSection_with_POST(self):
        response = self.client.post(ENDPOINT+'create/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_testTaskSection_with_GET(self):
        response = self.client.get(ENDPOINT)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_edit_testTaskSection_with_PATCH(self):
        response = self.client.patch(ENDPOINT+'edit/'+'3/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_testTaskSection_with_DELETE(self):
        response = self.client.delete(ENDPOINT+'delete/'+'3/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
