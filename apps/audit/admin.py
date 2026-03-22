from django.contrib import admin
from .models import AuditLog

# register AuditLog model with Django admin

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'actor',
        'target_user',
        'context',
        'action',
        'status',
        'timestamp'
    )
    list_filter = ('context', 'status', 'action')
    search_fields = (
        'actor__username',
        'target_user__username',
        'action'
    )
    ordering = ('-timestamp',)