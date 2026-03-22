from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Context
from .serializers import ContextSerializer


class ContextListView(ListAPIView):
    """
    Returns all available contexts.
    Authenticated users only.
    """

    queryset = Context.objects.all()
    serializer_class = ContextSerializer
    permission_classes = [IsAuthenticated]