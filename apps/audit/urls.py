from django.urls import path
from .views import AuditLogListView

urlpatterns = [
    # route for retrieving audit logs through the api
    path("logs/", AuditLogListView.as_view(), name="audit-logs"),
]