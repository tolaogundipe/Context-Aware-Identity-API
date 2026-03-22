from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin
from .models import User, Role, RolePermission, RoleContext


# role admin
# handles how roles are displayed and managed in admin panel
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)


# role permission admin
# manages what each role can do in different contexts
@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ("role", "context", "can_resolve_identity")
    list_filter = ("role", "context")
    search_fields = ("role__name", "context__name")


# role context admin
# defines which contexts are available for each role
@admin.register(RoleContext)
class RoleContextAdmin(admin.ModelAdmin):
    list_display = ("role", "context")
    list_filter = ("role", "context")
    search_fields = ("role__name", "context__name")


# custom user admin
# extends default django user admin with role and metadata
@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
            "fields": ("role", "is_verified"),
        }),
        ("System Metadata", {
            "fields": ("created_at",),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            "fields": ("role",),
        }),
    )

    readonly_fields = ("created_at",)

    list_display = ("username", "email", "role", "is_verified", "is_staff")