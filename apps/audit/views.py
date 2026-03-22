from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from .models import AuditLog
from .serializers import AuditLogSerializer
from .permissions import IsRegistryOfficer


# this view returns a list of audit logs
class AuditLogListView(ListAPIView):
    
    serializer_class = AuditLogSerializer

    # require user to be authenticated and have registry officer role
    permission_classes = [IsAuthenticated, IsRegistryOfficer]

    def get_queryset(self):
        # fetch audit logs with related user and context data to reduce queries
        return AuditLog.objects.select_related(
            "actor",
            "target_user",
            "context"
        ).order_by("-timestamp")[:50]  # return only the latest 50 logs