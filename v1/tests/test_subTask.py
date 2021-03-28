from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from task.models import SubTask
from v1.serializers.task_serializers import SubTaskSerializer

from .fake_data import *

ENDPOINT = "/api/v1/sub-tasks/"


class TestSubTask(APITestCase):
    print('Start SubTask TEST !!')


    def __count(self, person):
        return SubTask.objects.filter(person=person.id).count()


    def __add_subTask(self, person):
        task_folder = create_taskFolder(person)
        task_section = create_taskSection(person, task_folder)
        task = create_task(person, task_folder, task_section)
        return create_subTask(person, task)


    def setUp(self):
        create_taskData()
        self.person = create_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=self.person)


    def test_create_subTask_with_POST(self):
        task_folder = create_taskFolder(self.person)
        task_section = create_taskSection(self.person, task_folder)
        task = create_task(self.person,task_folder, task_section)
        
        data={
            "task":task.id,
            "person":self.person.id,
            "name":"new task is hard"
        }
        response = self.client.post(ENDPOINT + 'create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.__count(self.person), 1)

        sub_task = SubTask.objects.get(person=self.person.id, id=response.data["id"])
        self.assertEqual(data["name"], sub_task.name)


    def test_get_subTask_with_GET(self):
        sub_task = self.__add_subTask(self.person)
        self.assertEqual(self.__count(self.person), 1)

        response = self.client.get(ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        sub_tasks = SubTask.objects.filter(person=self.person.id)
        serializer = SubTaskSerializer(instance=sub_tasks, many=True)
        self.assertEqual(serializer.data, response.data)


    def test_edit_subTask_with_patch(self):
        sub_task = self.__add_subTask(self.person)
        self.assertEqual(self.__count(self.person), 1)

        edit_data={"name":"step-by-step"}
        response = self.client.patch(ENDPOINT + 'edit/' + str(sub_task.id) + "/", edit_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        edit_task = SubTask.objects.get(id=sub_task.id)
        self.assertEqual(response.data["name"], edit_task.name)


    def test_delete_subTask_with_DELETE(self):
        sub_task = self.__add_subTask(self.person)
        self.assertEqual(self.__count(self.person), 1)

        response = self.client.delete(ENDPOINT + 'delete/' + str(sub_task.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
