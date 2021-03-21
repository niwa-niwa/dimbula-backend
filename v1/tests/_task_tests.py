from rest_framework import response, status
from rest_framework.test import APITestCase, APIClient

from person.models import Person
from task.models import *
from v1.serializers._task_serializers import *

ROOT_URL = 'http://127.0.0.1:8000/api/v1/'
PERSON_URL = ROOT_URL + 'persons/'



class TaskTest(APITestCase):
    print("Start Task Test !!")


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


    def test_post_TaskFolder(self):
        new_taskfolder = {
            'firebase_id':"ThisIsId",
            'name':"TEST MAN",
            'email':"ccc@ccc.com",
            'provider_id':"facebook.com",
        }
        response = self.client.post(ROOT_URL + "taskfolders/create/", new_taskfolder)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # task_folder = TaskFolder.objects.all().first()
        # serializer = TaskFolderSerializer(task_folder)

        # self.assertTrue(response.data["id"])
        # self.assertEqual(response.data["name"], new_taskfolder["name"])
        # self.assertEqual(response.data["email"], new_taskfolder["email"])


    def test_get_TaskFolder(self):
        responce = self.client.get(ROOT_URL+"taskfolders/")
        # task_folders = TaskFolder.objects.all()
        # serializer = TaskFolderSerializer(task_folders, many=True)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        # self.assertEqual(responce.data, serializer.data)

    def test_patch_TaskFolder(self):
        response = self.client.patch(ROOT_URL+"taskfolders/edit/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_TaskFolder(self):
        response = self.client.delete(ROOT_URL+"taskfolders/delete/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)