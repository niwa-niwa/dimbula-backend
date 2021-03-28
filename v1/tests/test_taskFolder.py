from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from task.models import TaskFolder
from v1.serializers.task_serializers import *

from .fake_data import *

ROOT_URL = '/api/v1/'
TASKFOLDER = "task-folders/"


class TestTaskFolder(APITestCase):
    print("Start Task Test !!")


    def __count(self)->int:
        return TaskFolder.objects.filter(person=self.person).count()


    def setUp(self):
        create_taskData()
        self.person = create_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=self.person)


    def test_post_TaskFolder(self):
        new_taskfolder = {
            'name':"shopping",
            'person':self.person.id
        }
        response = self.client.post(ROOT_URL + TASKFOLDER + "create/", new_taskfolder)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.__count(), 1)

        task_folder = TaskFolder.objects.get(id=response.data["id"])
        self.assertEqual(task_folder.name, new_taskfolder["name"])
        self.assertEqual(task_folder.person.id, new_taskfolder["person"])


    def test_get_TaskFolder(self):
        create_taskFolder(self.person)
        self.assertEqual(self.__count(), 1)

        responce = self.client.get(ROOT_URL + TASKFOLDER)
        task_folders = TaskFolder.objects.filter(person=self.person.id)
        serializer = TaskFolderSerializer(task_folders, many=True)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(responce.data, serializer.data)


    def test_patch_TaskFolder(self):
        folder = create_taskFolder(self.person)
        self.assertEqual(self.__count(), 1)

        payload = {
            'name':"Edit_shopping",
            'person':self.person.id
        }
        response = self.client.patch(ROOT_URL+ TASKFOLDER + "edit/" + str(folder.id) + "/", payload)
        folder.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(folder.person, self.person)
        self.assertEqual(folder.name, payload['name'])


    def test_delete_TaskFolder(self):
        folder = create_taskFolder(self.person)
        self.assertEqual(self.__count(), 1)

        response = self.client.delete(ROOT_URL + TASKFOLDER + "delete/" + str(folder.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.__count(), 0)
