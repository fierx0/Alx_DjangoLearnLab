from django.urls import path
from .views import post_list

app_name = "blog"
urlpatterns = [
    path("", post_list, name="post_list"),
]

from django.urls import path
from .views import (
    post_list,
    LoginView, LogoutView, RegisterView,
    profile, profile_edit,
)

app_name = "blog"

urlpatterns = [
    path("", post_list, name="post_list"),

    # Auth
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", profile, name="profile"),
    path("profile/edit/", profile_edit, name="profile_edit"),
]
