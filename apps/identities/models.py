from django.db import models 
from django.conf import settings
from apps.contexts.models import Context


# this model represents a base identity that exists independently of context
class Identity(models.Model):
   
    # link identity to a user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='identities'
    )

    # type of name used (e.g. legal or preferred)
    name_type = models.CharField(
        max_length=50,
        help_text="e.g. legal, preferred"
    )

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Identity"
        verbose_name_plural = "Identities"

    def __str__(self):
        return f"{self.user.username} ({self.name_type})"


# this model represents how an identity is shown in a specific context
class IdentityProfile(models.Model):  

    # link profile to a base identity
    identity = models.ForeignKey(
        Identity,
        on_delete=models.CASCADE,
        related_name='profiles',
    )

    # link profile to a specific context
    context = models.ForeignKey(
        Context,
        on_delete=models.CASCADE,
        related_name='identity_profiles'
    )

    external_identifier = models.CharField(max_length=150)
    display_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            # ensure one identity has only one profile per context
            models.UniqueConstraint(
                fields=['identity', 'context'],
                name='unique_identity_context'
            ),
            # ensure external identifiers are unique within a context
            models.UniqueConstraint(
                fields=['context', 'external_identifier'],
                name='unique_identifier_per_context'
            )
        ]
        indexes = [
            # index to improve lookup performance during identity resolution
            models.Index(fields=['external_identifier', 'context']),
        ]

        # order profiles by context
        ordering = ['context']

    def __str__(self):
        return f"{self.identity.user.username} - {self.context.name}"