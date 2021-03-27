from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from person.models import Person
from task.models import TaskSection
from v1.serializers._task_serializers import *

from ._fake_data import *
from .test_taskFolder import create_taskFolder

ENDPOINT = '/api/v1/task-sections/'


class TestTaskSection(APITestCase):
    print('Start Task Section TEST !!')


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
        self.assertEqual(TaskSection.objects.filter(person=self.person.id).count(), 0)

        response = self.client.post(ENDPOINT+'create/',  new_section)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TaskSection.objects.filter(person=self.person.id).count(), 1)

        task_section = TaskSection.objects.get(id=response.data["id"])
        self.assertEqual(new_section["name"], task_section.name)
        self.assertEqual(new_section["taskFolder"], task_section.taskFolder.id)
        self.assertEqual(new_section["person"], task_section.person.id)


    def test_get_testTaskSection_with_GET(self):
        self.assertEqual(TaskSection.objects.filter(person=self.person.id).count(), 0)

        my_task_folder = create_taskFolder(self.person)
        my_task_section = create_taskSection(self.person, my_task_folder)
        self.assertEqual(TaskSection.objects.filter(person=self.person.id).count(), 1)

        response = self.client.get(ENDPOINT)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task_sections = TaskSection.objects.filter(person=self.person.id)
        serializer = TaskSectionSerializer(task_sections, many=True)
        self.assertEqual(serializer.data, response.data)


    def test_edit_testTaskSection_with_PATCH(self):
        response = self.client.patch(ENDPOINT+'edit/'+'3/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_delete_testTaskSection_with_DELETE(self):
        response = self.client.delete(ENDPOINT+'delete/'+'3/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
