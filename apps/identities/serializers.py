from rest_framework import serializers

# this serializer validates input data for identity resolution requests
class IdentityResolutionRequestSerializer(serializers.Serializer):
    
    external_identifier = serializers.CharField(required=True)
    context_id = serializers.IntegerField(required=True)


# this serializer formats the response for resolved identity data
class IdentityResolutionResponseSerializer(serializers.Serializer):

    display_name = serializers.CharField()
    external_identifier = serializers.CharField()
    email = serializers.EmailField(allow_null=True)
    context = serializers.CharField()