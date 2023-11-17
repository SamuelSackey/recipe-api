from django.urls import path

from users.views import *

app_name = "users"

urlpatterns = [
    path("create/", CreateUserView.as_view(), name="create"),
    path("login/", LoginView.as_view(), name="login"),
    path("me/", ManageAuthenticatedUserView.as_view(), name="me"),
]
