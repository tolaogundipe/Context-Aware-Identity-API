from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from apps.identities.models import Identity

from apps.users.models import RoleContext
from apps.identities.models import IdentityProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_or_update_identity(sender, instance, created, **kwargs):

    identity, created_identity = Identity.objects.get_or_create(
        user=instance,
        name_type="default",
        defaults={
            "first_name": instance.first_name or instance.username,
            "last_name": instance.last_name or ""
        }
    )

    updated = False

    if instance.first_name and identity.first_name != instance.first_name:
        identity.first_name = instance.first_name
        updated = True

    if instance.last_name and identity.last_name != instance.last_name:
        identity.last_name = instance.last_name
        updated = True

    if updated:
        identity.save()


@receiver(post_save, sender=User)
def create_identity_profiles(sender, instance, created, **kwargs):

    #create or update IdentityProfiles based on role + student_id.

    if not instance.role:
        return

    identity = Identity.objects.filter(user=instance).first()

    if not identity:
        return

    role_contexts = RoleContext.objects.filter(role=instance.role)

    for rc in role_contexts:
        profile, _ = IdentityProfile.objects.get_or_create(
            identity=identity,
            context=rc.context,
            defaults={
               "external_identifier": instance.student_id,
                "display_name": identity.first_name,
                "email": instance.email
            }
        )

        # update identifier if student_id now exists
        if instance.student_id and profile.external_identifier != instance.student_id:
            profile.external_identifier = instance.student_id
            profile.save()