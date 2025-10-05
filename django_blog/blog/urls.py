# blog/urls.py
from django.urls import path
from .views import (
    # CRUD views
    PostListView, PostDetailView, PostCreateView,
    PostUpdateView, PostDeleteView,
    # Auth/Profile views
    LoginView, LogoutView, RegisterView,
    profile, profile_edit,
)

app_name = "blog"

urlpatterns = [
    # Homepage → list posts
    path("", PostListView.as_view(), name="post_list"),

    # CRUD routes
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),

    # Authentication
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),

    # Profile management
    path("profile/", profile, name="profile"),
    path("profile/edit/", profile_edit, name="profile_edit"),
]
