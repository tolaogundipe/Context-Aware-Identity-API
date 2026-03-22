from rest_framework import serializers
from .models import Context

# this serializer converts context objects into api response format
class ContextSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Context
        fields = ["id", "name", "description"]