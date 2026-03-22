from apps.identities.models import IdentityProfile

for profile in IdentityProfile.objects.all():
    user = profile.identity.user
    if user.student_id:
        profile.external_identifier = user.student_id
        profile.save()

print("Updated identifiers")