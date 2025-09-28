from django.contrib import admin
from django.urls import path
from api.views import AuthorListCreateView, BookListCreateView, api_root

urlpatterns = [
    path("", api_root, name="api-root"),
    path("admin/", admin.site.urls),
    path("api/authors/", AuthorListCreateView.as_view(), name="authors"),
    path("api/books/", BookListCreateView.as_view(), name="books"),
]
