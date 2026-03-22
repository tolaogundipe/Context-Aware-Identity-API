from apps.identities.models import IdentityProfile
from apps.consent.models import Consent
from apps.audit.models import AuditLog
from apps.users.models import RolePermission

class IdentityResolutionService:

    @staticmethod
    def resolve_identity(actor, target_user, context):

        try:
            # get the active identity profile for this user in the given context
            profile = IdentityProfile.objects.filter(
                identity__user=target_user,
                context=context,
                is_active=True
            ).first()

            # check if the user has granted consent in this context
            if not Consent.objects.filter(
                user=target_user,
                context=context,
                is_granted=True
            ).exists():
                return {"error": "User has not granted consent in this context."}

            # check if the actor has permission to resolve identity in this context
            permission = RolePermission.objects.filter(
                role=actor.role,
                context=context,
                can_resolve_identity=True
            ).first()

            # deny access if no permission is found
            if not permission:
                return {"error": "You do not have permission to resolve identity in this context."}

            # apply fallback logic if no context-specific profile exists
            if profile:
                # use context-specific identity details
                display_name = profile.display_name
                external_identifier = profile.external_identifier
                email = profile.email or target_user.email
            else:
                # fall back to default user identity details
                display_name = target_user.first_name or target_user.username
                external_identifier = target_user.student_id
                email = target_user.email

            # log successful identity resolution
            AuditLog.objects.create(
                actor=actor,
                target_user=target_user,
                context=context,
                action="IDENTITY_RESOLUTION",
                status="SUCCESS"
            )

            # return identity data relevant to the context
            return {
                "display_name": display_name,
                "external_identifier": external_identifier,
                "email": email,
                "context": context.name
            }

        except Exception as e:
            # print error for debugging
            print("IDENTITY RESOLUTION ERROR:", str(e))

            # log failed identity resolution attempt
            AuditLog.objects.create(
                actor=actor,
                target_user=target_user if 'target_user' in locals() else None,
                context=context if 'context' in locals() else None,
                action="IDENTITY_RESOLUTION",
                status="FAILURE"
            )

            # return generic error message
            return {"error": "Unexpected error occurred during identity resolution."}

    @staticmethod
    def resolve_identity_by_identifier(actor, external_identifier, context_id):

        try:
            # get identity profile using external identifier and context
            profile = IdentityProfile.objects.get(
                external_identifier=external_identifier,
                context_id=context_id
            )

            # extract the user and context from the profile
            target_user = profile.identity.user
            context = profile.context

            # delegate to main identity resolution method
            return IdentityResolutionService.resolve_identity(
                actor=actor,
                target_user=target_user,
                context=context
            )

        except IdentityProfile.DoesNotExist:
             # return error if no identity profile is found
             return {"error": "No identity found for this identifier in the selected context."}