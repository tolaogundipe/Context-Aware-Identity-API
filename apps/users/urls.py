from django.urls import path
from .views import *

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
]