from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from apps.consent.models import Consent
from apps.users.models import RoleContext
from apps.contexts.models import Context

User = get_user_model()


# this signal runs after a new user is created
@receiver(post_save, sender=User)
def create_default_consents(sender, instance, created, **kwargs):
    
    # automatically create consent records based on user's role.
    # only contexts allowed for that role will be assigned.
    # and stop if this is not a new user

    if not created:
        return

    # if user has no role, do nothing
    if not instance.role:
        return

    # get all contexts allowed for this user's role
    role_contexts = RoleContext.objects.filter(role=instance.role)

    # create consent objects for each allowed context
    consents = [
        Consent(user=instance, context=rc.context, is_granted=True)
        for rc in role_contexts
    ]

    # save all consent records in one query for better performance
    Consent.objects.bulk_create(consents)


# this signal runs after a new context is created
@receiver(post_save, sender=Context)
def create_consent_for_new_context(sender, instance, created, **kwargs):
    
    # when a new context is created, assign it only to users
    # whose roles are allowed in that context.
    # and stop if it is not a new context

    if not created:
        return

    # get all role-context mappings for this context
    role_contexts = RoleContext.objects.filter(context=instance)

    # store consent objects before saving
    consents = []

    # loop through each role allowed in this context
    # and get all users with this role
    for rc in role_contexts:
        users = rc.role.users.all()

        # create consent for each user
        for user in users:
            consents.append(
                Consent(user=user, context=instance, is_granted=True)
            )

    # save all consent records in one query
    Consent.objects.bulk_create(consents)