from django.urls import path
from .views import BookList

urlpatterns = [
    path("books/", BookList.as_view(), name="book-list"),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Read-only list from previous step
    path('books/', BookList.as_view(), name='book-list'),
    # Full CRUD via ViewSet
    path('', include(router.urls)),
]
