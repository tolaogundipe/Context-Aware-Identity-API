from rest_framework.permissions import BasePermission

class IsLecturerOrRegistry(BasePermission):
    
    # allows access only to Lecturer or Registry Officer roles.

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return request.user.role.name in ["Lecturer", "Registry Officer"]