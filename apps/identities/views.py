from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.contexts.models import Context
from apps.users.models import User
from apps.identities.models import IdentityProfile

from .services import IdentityResolutionService
from .permissions import CanResolveIdentity
from .serializers import *

from drf_spectacular.utils import extend_schema, OpenApiExample

from apps.identities.models import IdentityProfile
from apps.contexts.models import Context


# this view handles identity resolution requests
class IdentityResolutionView(APIView):
    permission_classes = [IsAuthenticated, CanResolveIdentity]

    @extend_schema(
        request=IdentityResolutionRequestSerializer,
        responses=IdentityResolutionResponseSerializer,
        description="Resolves a user's identity within a specific context.",
    )
    def post(self, request):

        # validate input data from request
        serializer = IdentityResolutionRequestSerializer(data=request.data)

        # return error if input is invalid
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # extract validated data
        external_identifier = serializer.validated_data["external_identifier"]
        context_id = serializer.validated_data["context_id"]

        # delegate identity resolution logic to service layer
        result = IdentityResolutionService.resolve_identity_by_identifier(
            actor=request.user,
            external_identifier=external_identifier,
            context_id=context_id
        )

        # return success response if no error
        if result and "error" not in result:
            return Response(result, status=status.HTTP_200_OK)

        # return error response if resolution fails
        return Response(result, status=status.HTTP_400_BAD_REQUEST)
        
    

# this view allows a user to update their display name in a specific context
class UpdateDisplayNameView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):

        # get context id and new display name from request
        context_id = request.data.get("context_id")
        display_name = request.data.get("display_name")

        # validate required fields
        if not context_id or not display_name:
            return Response(
                {"error": "context_id and display_name are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # get the user's identity profile for the given context
            profile = IdentityProfile.objects.get(
                identity__user=request.user,
                context_id=context_id
            )

            # update the display name
            profile.display_name = display_name
            profile.save()

            # return success response
            return Response(
                {"message": "Display name updated successfully"},
                status=status.HTTP_200_OK
            )

        except IdentityProfile.DoesNotExist:
            # return error if user has no profile in that context
            return Response(
                {"error": "You do not have a profile in this context. Display name cannot be updated here."},
                status=status.HTTP_404_NOT_FOUND
            )