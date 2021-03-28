from rest_framework import status
from rest_framework.serializers import Serializer
from rest_framework.test import APITestCase, APIClient

from task.models import Task
from v1.serializers.task_serializers import TaskSerializer

from .fake_data import *

ENDPOINT = '/api/v1/tasks/'

class TestTask(APITestCase):
    print('Start Task TEST !!')


    def __count(self, person):
        return Task.objects.filter(person=person.id).count()


    def setUp(self):
        create_taskData()
        self.person = create_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=self.person)


    def test_create_task_with_POST(self):
        self.assertEqual(self.__count(self.person), 0)

        task_folder = create_taskFolder(self.person)
        task_section = create_taskSection(self.person, task_folder)
        data = {
            'name':'tsk-tsk',
            'taskFolder':task_folder.id,
            'taskSection':task_section.id,
            'person':self.person.id
        }

        response = self.client.post(ENDPOINT + 'create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.__count(self.person), 1)
        
        new_task = Task.objects.get(id=response.data["id"])
        self.assertEqual(data["name"], new_task.name)


    def test_get_task_with_GET(self):
        self.assertEqual(self.__count(self.person), 0)

        task_folder = create_taskFolder(self.person)
        task_section = create_taskSection(self.person, task_folder)
        task = create_task(self.person, task_folder, task_section)
        self.assertEqual(self.__count(self.person), 1);

        response = self.client.get(ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        tasks = Task.objects.filter(person=self.person.id)
        serializer = TaskSerializer(instance=tasks, many=True)
        self.assertEqual(response.data, serializer.data)


    def test_edit_task_with_PATCH(self):
        self.assertEqual(self.__count(self.person), 0)

        task_folder = create_taskFolder(self.person)
        task_section = create_taskSection(self.person, task_folder)
        task = create_task(self.person, task_folder, task_section)
        self.assertEqual(self.__count(self.person), 1)

        data = {"name":'edited name'}
        response = self.client.patch(ENDPOINT + 'edit/' + str(task.id) + '/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        edit_task = Task.objects.get(pk=task.id)
        self.assertEqual(edit_task.name, data["name"])


    def test_delete_task_with_DELETE(self):
        task_folder = create_taskFolder(self.person)
        task_section = create_taskSection(self.person, task_folder)
        task = create_task(self.person, task_folder, task_section)
        self.assertEqual(self.__count(self.person), 1)

        response = self.client.delete(ENDPOINT + 'delete/' + str(task.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(self.__count(self.person), 0)
