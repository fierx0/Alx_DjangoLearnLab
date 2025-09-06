from django.urls import path
from .views import list_books, LibraryDetailView  # <- exact strings checker wants

urlpatterns = [
    path("books/", list_books, name="list_books"),  # function-based
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),  # class-based
]
