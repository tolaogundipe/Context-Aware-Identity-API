from rest_framework.test import APITestCase 
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.users.models import Role
from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()

# user list api tests
# tests access control and filtering for user endpoint
class UserListAPITest(APITestCase):

    # setup test data
    # creates roles, users, and base endpoint
    def setUp(self):
        self.student_role = Role.objects.create(name="Student")
        self.lecturer_role = Role.objects.create(name="Lecturer")
        self.registry_role = Role.objects.create(name="Registry Officer")

        self.student = User.objects.create_user(
            username="student1",
            password="testpass",
            role=self.student_role
        )

        self.lecturer = User.objects.create_user(
            username="lecturer1",
            password="testpass",
            role=self.lecturer_role
        )

        self.registry = User.objects.create_user(
            username="registry1",
            password="testpass",
            role=self.registry_role
        )

        self.base_url = "/api/users/"


    # test lecturer access
    # ensures lecturer can view all users
    def test_lecturer_can_view_all_users(self):
        token = RefreshToken.for_user(self.lecturer).access_token

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(token)}"
        )

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)


    # test filtering by role
    # ensures users can be filtered using query parameter
    def test_filter_users_by_role(self):
        token = RefreshToken.for_user(self.lecturer).access_token

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(token)}"
        )

        response = self.client.get(f"{self.base_url}?role=Student")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    # test access restriction
    # ensures students cannot view user list
    def test_student_cannot_view_users(self):
        token = RefreshToken.for_user(self.student).access_token

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(token)}"
        )

        response = self.client.get(self.base_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)