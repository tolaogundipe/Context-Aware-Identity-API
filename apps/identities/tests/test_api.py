from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

from apps.contexts.models import Context
from apps.identities.models import Identity, IdentityProfile
from apps.consent.models import Consent
from apps.users.models import Role, RolePermission

from rest_framework_simplejwt.tokens import RefreshToken


User = get_user_model()


# this test class checks the identity resolution api endpoint
class IdentityResolutionAPITest(APITestCase):

    def setUp(self):
        # roles
        self.student_role = Role.objects.create(name="Student")
        self.lecturer_role = Role.objects.create(name="Lecturer")

        # users
        self.student = User.objects.create_user(
            username="student1",
            password="testpass",
            role=self.student_role
        )

        # create a lecturer who will perform identity resolution
        self.lecturer = User.objects.create_user(
            username="lecturer1",
            password="testpass",
            role=self.lecturer_role
        )

        # context where identity will be resolved
        self.context = Context.objects.create(name="Student Portal")

        # assign permission so lecturer can resolve identity in this context
        RolePermission.objects.create(
            role=self.lecturer_role,
            context=self.context,
            can_resolve_identity=True
        )

        # create base identity for the student
        self.identity = Identity.objects.create(
            user=self.student,
            name_type="default",
            first_name="Student",
            last_name="One"
        )

        # create identity profile for this context
        IdentityProfile.objects.create(
            identity=self.identity,
            context=self.context,
            external_identifier="STD-001",
            display_name="Student One",
            is_active=True
        )

        # create consent so identity can be shared
        Consent.objects.create(
            user=self.student,
            context=self.context,
            is_granted=True
        )

        # generate jwt token for lecturer authentication
        refresh = RefreshToken.for_user(self.lecturer)
        self.access_token = str(refresh.access_token)

        # define api endpoint for identity resolution
        self.url = reverse("resolve-identity")

    def test_identity_resolution_success(self):
        # attach jwt token to request header
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.access_token}"
        )

        # send post request with identifier and context
        response = self.client.post(
            self.url,
            {
                "external_identifier": "STD-001",
                "context_id": self.context.id
            },
            format="json"
        )

        # check that request is successful (200 ok)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # check that correct identity data is returned
        self.assertEqual(response.data["external_identifier"], "STD-001")

    def test_identity_resolution_requires_authentication(self):
        # send request without authentication
        response = self.client.post(
            self.url,
            {
                "external_identifier": "STD-001",
                "context_id": self.context.id
            },
            format="json"
        )

        # check that access is denied (401 unauthorized)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)