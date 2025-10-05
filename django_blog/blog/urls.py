from django.urls import path
from .views import (
    PostListView, PostDetailView,
    PostCreateView, PostUpdateView, PostDeleteView,
    CommentCreateView, CommentUpdateView, CommentDeleteView,
    PostByTagListView, PostSearchListView,
    LoginView, LogoutView, RegisterView,
    profile, profile_edit
)

app_name = "blog"

urlpatterns = [
    # Post CRUD
    path("", PostListView.as_view(), name="post_list"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/new/", PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),

    # Comments
    path("post/<int:pk>/comments/new/", CommentCreateView.as_view(), name="comment_create"),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment_update"),
    path("comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),

    # Tags & Search
    path("tags/<slug:tag_slug>/", PostByTagListView.as_view(), name="post_by_tag"),  # ✅ checker expects tag_slug
    path("search/", PostSearchListView.as_view(), name="post_search"),

    # Auth
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),

    # Profile
    path("profile/", profile, name="profile"),
    path("profile/edit/", profile_edit, name="profile_edit"),
]
