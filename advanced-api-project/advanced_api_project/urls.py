from django.contrib import admin
from django.urls import path, include
from api.views import AuthorListCreateView, BookListCreateView, api_root

urlpatterns = [
    path("", api_root, name="api-root"),
    path("admin/", admin.site.urls),
    # existing endpoints
    path("api/authors/", AuthorListCreateView.as_view(), name="authors"),
    path("api/books/", BookListCreateView.as_view(), name="books"),
    # NEW generic Book endpoints
    path("api/", include("api.urls")),
]
