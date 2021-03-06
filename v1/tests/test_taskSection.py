from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from task.models import TaskSection
from v1.serializers.task_serializers import *

from .fake_data import *

ENDPOINT = '/api/v1/task-sections/'


class TestTaskSection(APITestCase):
    print('Start Task Section TEST !!')

    def __count(self):
        return TaskSection.objects.filter(person=self.person).count()


    def __create_taskSection(self):
        task_folder = create_taskFolder(self.person)
        return create_taskSection(self.person, task_folder)


    def setUp(self):
        create_taskData()
        self.person = create_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=self.person)


    def test_create_taskSection_with_POST(self):
        task_folder = create_taskFolder(self.person)
        new_section = {
            'name':'new_section',
            'taskFolder':task_folder.id,
            "person":self.person.id,
        }
        response = self.client.post(ENDPOINT+'create/',  new_section)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.__count(), 1)

        task_section = TaskSection.objects.get(id=response.data["id"])
        self.assertEqual(new_section["name"], task_section.name)
        self.assertEqual(new_section["taskFolder"], task_section.taskFolder.id)
        self.assertEqual(new_section["person"], task_section.person.id)


    def test_get_testTaskSection_with_GET(self):
        task_section = self.__create_taskSection()
        self.assertEqual(self.__count(), 1)

        response = self.client.get(ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task_sections = TaskSection.objects.filter(person=self.person.id)
        serializer = TaskSectionSerializer(task_sections, many=True)
        self.assertEqual(serializer.data, response.data)


    def test_edit_testTaskSection_with_PATCH(self):
        task_section = self.__create_taskSection()
        self.assertEqual(self.__count(), 1)

        edit_data = {"name":"pop-edit"}
        response = self.client.patch(ENDPOINT+'edit/' + str(task_section.id) + '/',edit_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        new_section = TaskSection.objects.get(id=task_section.id)
        self.assertEqual(edit_data["name"], new_section.name)


    def test_delete_testTaskSection_with_DELETE(self):
        task_section = self.__create_taskSection()
        self.assertEqual(self.__count(), 1)

        response = self.client.delete(ENDPOINT+'delete/'+ str(task_section.id) + '/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TaskSection.objects.filter(person=self.person).count(), 0)

