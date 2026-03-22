from django.db import models
from django.conf import settings
from apps.contexts.models import Context


# this model stores audit logs for identity resolution and access events
class AuditLog(models.Model): 
    
    # the user who performed the action (for example lecturer or registry officer)
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='performed_actions'
    )

    # the user whose identity was accessed or resolved
    target_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_entries'
    )

    # the context where the action happened
    context = models.ForeignKey(
        Context,
        on_delete=models.SET_NULL,
        null=True
    )

    # the type of action performed 
    action = models.CharField(
        max_length=150,
        help_text="Action performed (e.g., IDENTITY_RESOLUTION)"
    )

    status = models.CharField(
        max_length=50,
        help_text="Result of action (SUCCESS / FAILURE)"
    )

    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(
        blank=True,
        null=True,
        help_text="Optional structured event details"
    )

    class Meta:
        # order logs by newest first
        ordering = ['-timestamp']

        # name shown in django admin
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"

    def __str__(self):
        # return a readable string representation of the log
        return f"{self.actor} → {self.action} ({self.status})"