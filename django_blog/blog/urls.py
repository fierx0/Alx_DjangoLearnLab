from django.urls import path
from .views import (
    # posts
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    # comments
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    # auth/profile
    LoginView, LogoutView, RegisterView, profile, profile_edit,
)

app_name = "blog"

urlpatterns = [
    # home/list
    path("", PostListView.as_view(), name="post_list"),

    # post CRUD (singular paths per checker)
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),

    # comments
    path("post/<int:post_id>/comments/new/", CommentCreateView.as_view(), name="comment_create"),
    path("comments/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment_update"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),

    # auth/profile
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", profile, name="profile"),
    path("profile/edit/", profile_edit, name="profile_edit"),
]
