from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from apps.users.models import Role
from apps.audit.models import AuditLog
from rest_framework_simplejwt.tokens import RefreshToken

# get the user model
User = get_user_model()

# this test class checks access control for audit log endpoints
class AuditLogAPITest(APITestCase):

    def setUp(self):
        # create roles for testing permissions
        self.registry_role = Role.objects.create(name="Registry Officer")
        self.student_role = Role.objects.create(name="Student")

        # create a registry user who should have access
        self.registry = User.objects.create_user(
            username="registry1",
            password="testpass",
            role=self.registry_role
        )

        # create a student user who should not have access
        self.student = User.objects.create_user(
            username="student1",
            password="testpass",
            role=self.student_role
        )

        # create a sample audit log entry
        AuditLog.objects.create(
            actor=self.registry,
            target_user=self.student,
            action="TEST_ACTION",
            status="SUCCESS"
        )

        # define the api endpoint for audit logs
        self.url = "/api/audit/logs/"

    def test_registry_can_view_audit_logs(self):
        # generate jwt token for registry user
        token = RefreshToken.for_user(self.registry).access_token

        # attach token to request header
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(token)}"
        )

        # send get request to audit logs endpoint
        response = self.client.get(self.url)

        # check that access is allowed (200 ok)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_student_cannot_view_audit_logs(self):
        # generate jwt token for student user
        token = RefreshToken.for_user(self.student).access_token

        # attach token to request header
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {str(token)}"
        )

        # send get request to audit logs endpoint
        response = self.client.get(self.url)

        # check that access is denied (403 forbidden)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)