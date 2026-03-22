from rest_framework.permissions import BasePermission


# this permission class restricts access to only registry officers
class IsRegistryOfficer(BasePermission):
    
    # allows access only to Registry Officer role.
    def has_permission(self, request, view):
        # check if the user is authenticated
        if not request.user.is_authenticated:
            return False

        # allow access only if the user role is registry officer
        return request.user.role.name == "Registry Officer"