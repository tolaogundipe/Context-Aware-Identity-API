from django.urls import path
from .views import *

urlpatterns = [
    path("resolve/", IdentityResolutionView.as_view(), name="resolve-identity"),
    path("update-display-name/", UpdateDisplayNameView.as_view()),
]