from django.urls import path
from .views import ContextListView

urlpatterns = [
    path("", ContextListView.as_view(), name="context-list"),
]