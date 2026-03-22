from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Context
from .serializers import ContextSerializer


# this view returns a list of available contexts
# returns all available contexts for authenticated users only.
class ContextListView(ListAPIView):

    # fetch all context records ordered by id
    queryset = Context.objects.all().order_by("id")

    # use context serializer to format the response
    serializer_class = ContextSerializer

    # restrict access to authenticated users only
    permission_classes = [IsAuthenticated]