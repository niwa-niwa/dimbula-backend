from django.db import models
from django.test import TestCase
from rest_framework import response, serializers, status
from rest_framework.test import APITestCase
from user.models import User
from .serializers import UserSerializer

USER_URL = 'http://127.0.0.1:8000/api/v1/users/'

# Create your tests here.
class UserTest(APITestCase):


    def test_getUser(self):
        # print(USER_URL)
        responce = self.client.get(USER_URL)
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        self.assertEqual(responce.status_code, status.HTTP_200_OK)
        self.assertEqual(responce.data, serializer.data)


    def test_createUser(self):
        new_user = {
            'id':"ThisIsId",
            'name':"TEST MAN",
            'email_verified':True,
            'photo_url':"http://www.aaa.com",
            'provider_id':"facebook.com",
            'is_admin':True,
        }

        response = self.client.post(USER_URL + "create/", new_user)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.all().first()
        serializer = UserSerializer(user)

        self.assertEqual(response.data["id"], new_user["id"])
        self.assertEqual(response.data["name"], new_user["name"])
        self.assertEqual(response.data["email_verified"], new_user["email_verified"])
        self.assertEqual(response.data["photo_url"], new_user["photo_url"])
        self.assertEqual(response.data["provider_id"], new_user["provider_id"])
        self.assertEqual(response.data["is_admin"], new_user["is_admin"])
