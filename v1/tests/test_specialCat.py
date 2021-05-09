from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from task.models import TaskFolder
from v1.serializers.task_serializers import *

from .fake_data import *

ROOT_URL = '/api/v1/'
INBOX = "inbox/"


class TestInbox(APITestCase):
    print("Start Inbox Test !!")

    def __count(self)->int:
        return Task.objects.filter(person=self.person.id).count()


    def __create_task(self)->Task:
        task_folder = create_taskFolder(self.person)
        task_section = create_taskSection(self.person, task_folder)
        return create_task(self.person, task_folder, task_section)


    def setUp(self):
        create_taskData()
        self.person = create_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=self.person)


    def test_get_inbox(self):
        self.assertEqual(self.__count(), 0)
        task = self.__create_task()
        self.assertEqual(self.__count(), 1)

        data = {
            'name':'tsk-tsk',
            'person':self.person.id
        }
        self.client.post(ROOT_URL+ 'tasks/create/', data)
        data = {
            'name':'tsk-tsk-tsk',
            'person':self.person.id
        }
        self.client.post(ROOT_URL+ 'tasks/create/', data)
        self.assertEqual(self.__count(), 3)

        inbox = self.client.get(ROOT_URL + 'inbox/')
        self.assertEqual(inbox.status_code, status.HTTP_200_OK)

        self.assertEqual(len(inbox.data), 2)