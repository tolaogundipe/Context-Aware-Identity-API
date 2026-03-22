from django.db import models
from django.conf import settings
from apps.contexts.models import Context

# this model stores whether a user has given consent for a context
# represents a user's consent for a context to access identity data.
class Consent(models.Model):

    # link consent to a specific user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='consents'
    )

    # link consent to a specific context (e.g. learning platform)
    context = models.ForeignKey(
        Context,
        on_delete=models.CASCADE,
        related_name='consents'
    )

    # indicates whether consent is currently granted or not
    is_granted = models.BooleanField(
        default=True
    )

    # stores when consent was first given
    granted_at = models.DateTimeField(
        auto_now_add=True
    )

    # stores when consent was revoked
    revoked_at = models.DateTimeField(
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ('user', 'context')
        verbose_name = "Consent"
        verbose_name_plural = "Consents"

    def __str__(self):
        # return a readable representation of the consent status
        status = "Granted" if self.is_granted else "Revoked"
        return f"{self.user.username} - {self.context.name} ({status})"