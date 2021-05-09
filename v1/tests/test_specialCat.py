import datetime
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

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
        self.__create_task()
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

        tasks = self.client.get(ROOT_URL + 'inbox/')
        self.assertEqual(tasks.status_code, status.HTTP_200_OK)

        self.assertEqual(len(tasks.data), 2)

    
class TestToday(APITestCase):
    print("Start Today Test !!")

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


    def test_get_today(self):
        self.assertEqual(self.__count(), 0)
        self.__create_task()
        self.assertEqual(self.__count(), 1)

        data = {
            'name':'tsk-tsk',
            'person':self.person.id,
            'due_date':datetime.datetime.now()
        }
        self.client.post(ROOT_URL+ 'tasks/create/', data)
        data = {
            'name':'tsk-tsk-tsk',
            'person':self.person.id,
            'due_date':datetime.datetime.now()
        }
        self.client.post(ROOT_URL+ 'tasks/create/', data)
        self.assertEqual(self.__count(), 3)

        tasks = self.client.get(ROOT_URL + 'today/')
        self.assertEqual(tasks.status_code, status.HTTP_200_OK)
        self.assertEqual(len(tasks.data), 2)


class TestStars(APITestCase):
    print("Start Stars Test !!")

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


    def test_get_stars(self):
        self.assertEqual(self.__count(), 0)
        self.__create_task()
        self.assertEqual(self.__count(), 1)

        data = {
            'name':'tsk-tsk',
            'person':self.person.id,
            'is_star':True
        }
        self.client.post(ROOT_URL+ 'tasks/create/', data)
        data = {
            'name':'tsk-tsk-tsk',
            'person':self.person.id,
            'is_star':True
        }
        self.client.post(ROOT_URL+ 'tasks/create/', data)
        self.assertEqual(self.__count(), 3)

        tasks = self.client.get(ROOT_URL + 'stars/')
        self.assertEqual(tasks.status_code, status.HTTP_200_OK)
        self.assertEqual(len(tasks.data), 2)


class TestAllTasks(APITestCase):
    print("Start AllTasks Test !!")

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


    def test_get_stars(self):
        self.assertEqual(self.__count(), 0)
        self.__create_task()
        self.assertEqual(self.__count(), 1)

        data = {
            'name':'tsk-tsk',
            'person':self.person.id,
        }
        self.client.post(ROOT_URL+ 'tasks/create/', data)
        data = {
            'name':'tsk-tsk-tsk',
            'person':self.person.id,
            'is_star':True
        }
        self.client.post(ROOT_URL+ 'tasks/create/', data)
        self.assertEqual(self.__count(), 3)

        tasks = self.client.get(ROOT_URL + 'all-tasks/')
        self.assertEqual(tasks.status_code, status.HTTP_200_OK)
        self.assertEqual(len(tasks.data), 3)
        