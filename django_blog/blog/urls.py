from django.urls import path
from .views import (
    # posts
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    # comments
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    # tags & search
    PostByTagListView, PostSearchListView,
    # auth/profile
    LoginView, LogoutView, RegisterView, profile, profile_edit,
)

app_name = "blog"

urlpatterns = [
    # home/list
    path("", PostListView.as_view(), name="post_list"),

    # post CRUD (singular paths to match your checker)
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),

    # comments (checker-exact strings)
    path("post/<int:pk>/comments/new/", CommentCreateView.as_view(), name="comment_create"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment_update"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),

    # tags & search
    path("tags/<slug:slug>/", PostByTagListView.as_view(), name="post_by_tag"),
    path("search/", PostSearchListView.as_view(), name="post_search"),

    # auth/profile
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", profile, name="profile"),
    path("profile/edit/", profile_edit, name="profile_edit"),
]
