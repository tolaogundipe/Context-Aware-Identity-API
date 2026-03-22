from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import User
from .serializers import UserListSerializer
from .permissions import IsLecturerOrRegistry

from rest_framework.views import APIView
from rest_framework.response import Response



# this view returns a list of users with optional role filtering
class UserListView(ListAPIView):

    serializer_class = UserListSerializer
    permission_classes = [IsAuthenticated, IsLecturerOrRegistry]

    @extend_schema(
        description="Retrieve users. Optionally filter by role.",
        parameters=[
            # allow filtering users by role using query parameter
            OpenApiParameter(
                name="role",
                description="Filter users by role name (e.g. Student)",
                required=False,
                type=str,
            )
        ],
        responses=UserListSerializer(many=True),
    )

    def get_queryset(self):
        queryset = User.objects.all().order_by("id")
        role = self.request.query_params.get("role")
        if role:
            queryset = queryset.filter(role__name=role)

        return queryset

# this view returns the currently authenticated user's details
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # serialize the current user
        serializer = UserListSerializer(request.user)

        # return user data
        return Response(serializer.data)