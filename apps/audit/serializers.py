from rest_framework import serializers
from .models import AuditLog


# this serializer converts audit log objects into api response format
class AuditLogSerializer(serializers.ModelSerializer):

    actor = serializers.CharField(source="actor.username", read_only=True)
    target_user = serializers.CharField(source="target_user.username", read_only=True)
    context = serializers.CharField(source="context.name", read_only=True)

    class Meta:
        model = AuditLog

        # define the fields to include in the api response
        fields = [
            "id",
            "actor",
            "target_user",
            "context",
            "action",
            "status",
            "timestamp",
        ]