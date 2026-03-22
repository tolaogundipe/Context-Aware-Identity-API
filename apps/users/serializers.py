from rest_framework import serializers 
from .models import User

# this serializer converts user objects into api response format
class UserListSerializer(serializers.ModelSerializer):
    
    role = serializers.CharField(source="role.name")

    class Meta:
        model = User

        # define the fields to include in the api response
        fields = [
            "id",
            "username",
            "first_name",  
            "last_name",    
            "email",
            "student_id",  
            "role"
        ]