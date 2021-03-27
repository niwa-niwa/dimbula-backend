from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from person.models import Person
from task.models import TaskFolder
from v1.serializers._task_serializers import *

ROOT_URL = '/api/v1/'
TASKFOLDER = "task-folders/"


def create_person() -> Person:
    return Person.objects.create(
        firebase_id="1_firebase_user_uid",
        name="aa_test_name",
        email="testaa_email@adb.com",
        email_verified=True,
        provider_id="google.com"
    )

def create_taskFolder(person: Person) -> TaskFolder:
    return TaskFolder.objects.create(
        name="shopping",
        person=person
    )


class TestTaskFolder(APITestCase):
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
            'name':"shopping",
            'person':self.person.id
        }

        response = self.client.post(ROOT_URL + TASKFOLDER + "create/", new_taskfolder)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        task_folder = TaskFolder.objects.get(id=response.data["id"])

        self.assertEqual(task_folder.name, new_taskfolder["name"])

        self.assertEqual(task_folder.person.id, new_taskfolder["person"])


    def test_get_TaskFolder(self):

        create_taskFolder(self.person)

        responce = self.client.get(ROOT_URL + TASKFOLDER)
        
        task_folders = TaskFolder.objects.filter(person=self.person.id)

        serializer = TaskFolderSerializer(task_folders, many=True)
        
        self.assertEqual(responce.status_code, status.HTTP_200_OK)

        self.assertEqual(responce.data, serializer.data)


    def test_patch_TaskFolder(self):

        folder = create_taskFolder(self.person)
        
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

        self.assertEqual(1, TaskFolder.objects.count())

        response = self.client.delete(ROOT_URL + TASKFOLDER + "delete/" + str(folder.id) + "/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(0, TaskFolder.objects.count())
