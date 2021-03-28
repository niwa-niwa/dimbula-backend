from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from task.models import SubTask
from v1.serializers.task_serializers import SubTackSerializer

from .fake_data import *

ENDPOINT = "/api/v1/sub-tasks/"


class SubTask(APITestCase):
    print('Start SubTask TEST !!')


    def __count(self, person):
        return SubTask.objects.filter(person=person.id).count()


    def setUp(self):
        create_taskData()
        self.person = create_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=self.person)


    def test_create_subTask_with_POST(self):
        response = self.client.post(ENDPOINT + 'create/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_subTask_with_GET(self):
        response = self.client.get(ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_edit_subTask_with_patch(self):
        response = self.client.patch(ENDPOINT + 'edit/' + "1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_subTask_with_DELETE(self):
        response = self.client.delete(ENDPOINT + 'delete/' + "1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        