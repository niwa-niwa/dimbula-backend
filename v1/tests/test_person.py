from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from person.models import Person
from v1.serializers import PersonSerializer

PERSON_URL = '/api/v1/persons/'

def create_admin() -> Person:
    return Person.objects.create(
            firebase_id="admin_firebase_user_uid",
            name="test_name_admin",
            email="test_email_admin@adb.com",
            email_verified=True,
            provider_id="google.com",
            is_admin=True,
    )

def create_persons() -> list:
    person_a = Person.objects.create(
        firebase_id="person_a_firebase_user_uid",
        name="test_name_person_a",
        email="test_email_person_a@adb.com",
        email_verified=True,
        provider_id="google.com",
        is_admin=True,
    )
    person_b = Person.objects.create(
        firebase_id="person_b_firebase_user_uid",
        name="test_name_person_b",
        email="test_email_person_b@adb.com",
        email_verified=True,
        provider_id="google.com",
        is_admin=False,
    )
    person_c = Person.objects.create(
        firebase_id="person_c_firebase_user_uid",
        name="test_name_person_c",
        email="test_email_person_c@adb.com",
        email_verified=False,
        provider_id="google.com",
        is_admin=False,
    )
    return [person_a, person_b, person_c]


# Create your tests here.
class TestPerson(APITestCase):

    print("Start Person Test !!")
    
    def setUp(self):
        self.person = create_admin()
        self.client = APIClient()
        self.client.force_authenticate(user=self.person)

    def test_getUser(self):
        create_persons()
        responce = self.client.get(PERSON_URL)
        person = Person.objects.all()
        serializer = PersonSerializer(person, many=True)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(responce.data, serializer.data)


    def test_createUser(self):
        new_user = {
            'firebase_id':"ThisIsId",
            'name':"TEST MAN",
            'email':"ccc@ccc.com",
            'provider_id':"facebook.com",
        }

        response = self.client.post(PERSON_URL + "create/", new_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(response.data["id"])
        self.assertEqual(response.data["name"], new_user["name"])
        self.assertEqual(response.data["email"], new_user["email"])
