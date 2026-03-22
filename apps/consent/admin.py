from django.contrib import admin
from .models import Consent

# register Consent model with Django admin

@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'context',
        'is_granted',
        'granted_at'
    )
    list_filter = ('context', 'is_granted')
    search_fields = ('user__username',)
    ordering = ('context',)