from django.contrib import admin
from .models import Context

# register Context model with Django admin

@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)