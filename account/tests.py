from .models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import RequestsClient

TEST_USER = {"email": "agent@gmail.com", "name": "testagent",
                "password": "password", "phone": "1000000000"}

class UserRegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {"email": "testcase@gmail.com", "name": "testuser",
                "password": "password", "phone": "0000000000"}
        response = self.client.post("/api/auth/register", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AgentRegistrationTestCase(APITestCase):
    def test_agentregistration(self):
        data = {"email": "agent@gmail.com", "name": "testagent",
                "password": "password", "phone": "1000000000"}
        response = self.client.post("/api/auth/agentregister", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTestCase(APITestCase):
    
    
    def setup(self):
        data = {"email": "testcase1@gmail.com","password": "password" ,"name": "testuser",
                "phone": "0000000000"}
        x = User.objects.create_user(**data)
        print(x)
        x.save()
        self.requests = RequestsClient()
    def test_login(self):
        temp = APIClient()
        data = {"email":TEST_USER['email'],"password":TEST_USER['password']}
        resp = temp.post("/token-auth/", data=data, follow=True)
        response = self.client.post("/api/auth/login", data)
        print(response.content)

        