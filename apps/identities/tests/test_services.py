from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.contexts.models import Context
from apps.identities.models import Identity, IdentityProfile
from apps.consent.models import Consent
from apps.identities.services import IdentityResolutionService
from apps.users.models import Role, RolePermission


User = get_user_model()


# this test class checks the identity resolution service logic directly
class IdentityResolutionServiceTest(TestCase):

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

        # create a lecturer who will resolve identity
        self.lecturer = User.objects.create_user(
            username="lecturer1",
            password="testpass",
            role=self.lecturer_role
        )

        # context where identity resolution will happen
        self.context = Context.objects.create(name="Student Portal")

        # assign permission so lecturer can resolve identity
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
        self.profile = IdentityProfile.objects.create(
            identity=self.identity,
            context=self.context,
            external_identifier="STD-001",
            display_name="Student One",
            is_active=True
        )

        # create consent so identity can be accessed
        self.consent = Consent.objects.create(
            user=self.student,
            context=self.context,
            is_granted=True
        )

    def test_identity_resolution_success(self):
        # call the service directly
        result = IdentityResolutionService.resolve_identity(
            actor=self.lecturer,
            target_user=self.student,
            context=self.context
        )

        # check that result is returned
        self.assertIsNotNone(result)

        # check that correct identifier is returned
        self.assertEqual(result["external_identifier"], "STD-001")

    def test_identity_resolution_fails_without_consent(self):
        # remove consent to simulate privacy restriction
        self.consent.delete()

        # call the service again
        result = IdentityResolutionService.resolve_identity(
            actor=self.lecturer,
            target_user=self.student,
            context=self.context
        )

        # check that error is returned when consent is missing
        self.assertIn("error", result)

    def test_identity_resolution_fallback_without_profile(self):
        # remove profile to trigger fallback logic
        self.profile.delete()

        # call the service again
        result = IdentityResolutionService.resolve_identity(
            actor=self.lecturer,
            target_user=self.student,
            context=self.context
        )

        # check that fallback still returns a result
        self.assertIsNotNone(result)

        # check that fallback uses default identifier
        self.assertEqual(result["external_identifier"], self.student.student_id)