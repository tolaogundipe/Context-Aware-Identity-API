from django.contrib import admin
from .models import Identity, IdentityProfile

# register Identity model with Django admin

@admin.register(Identity)
class IdentityAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'name_type',
        'first_name',
        'last_name',
        'created_at'
    )
    list_filter = ('name_type',)
    search_fields = ('user__username', 'first_name', 'last_name')


# register IdentityProfile model with Django admin

@admin.register(IdentityProfile)
class IdentityProfileAdmin(admin.ModelAdmin):
    list_display = (
        'identity',
        'get_user',
        'context',
        'external_identifier',
        'is_active',
        'created_at'
    )

    list_filter = ('context', 'is_active')

    search_fields = (
        'identity__user__username',
        'identity__first_name',
        'external_identifier',
        'email'
    )

    ordering = ('context',)

    def get_user(self, obj):
        return obj.identity.user.username

    get_user.short_description = 'User'