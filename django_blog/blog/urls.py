from django.urls import path
from .views import (
    PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView,
    # your existing auth views also stay here if you added them earlier
    LoginView, LogoutView, RegisterView, profile, profile_edit,
)

app_name = "blog"

urlpatterns = [
    # home/list
    path("", PostListView.as_view(), name="post_list"),
    path("posts/", PostListView.as_view(), name="post_list_alt"),

    # CRUD
    path("posts/new/", PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="post_update"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),

    # auth/profile (from your previous task)
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", profile, name="profile"),
    path("profile/edit/", profile_edit, name="profile_edit"),
]
