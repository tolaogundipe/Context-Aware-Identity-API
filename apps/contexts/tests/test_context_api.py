from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.contexts.models import Context
from apps.users.models import Role
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


# this test class checks the context list api endpoint
class ContextAPITest(APITestCase):

    def setUp(self):
        # create a role for the test user
        self.role = Role.objects.create(name="Student")

        # create a user with the role
        self.user = User.objects.create_user(
            username="user1",
            password="testpass",
            role=self.role
        )

        # create a sample context
        self.context = Context.objects.create(name="Student Portal")

        # generate jwt token for authentication
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # define the api endpoint for contexts
        self.url = "/api/contexts/"

    def test_context_list_authenticated(self):
        # attach jwt token to request header
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        # send get request to contexts endpoint
        response = self.client.get(self.url)

        # check that request is successful (200 ok)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check that one context is returned
        self.assertEqual(len(response.data["results"]), 1)

    def test_context_list_requires_authentication(self):
        # send request without authentication
        response = self.client.get(self.url)

        # check that access is denied (401 unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)