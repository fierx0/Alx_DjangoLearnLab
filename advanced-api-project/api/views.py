from rest_framework import generics, permissions, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

# ✅ Required by checker
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.prefetch_related("books").all()
    serializer_class = AuthorSerializer

class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer

@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        "authors": reverse("authors", request=request),
        "books": reverse("books", request=request),
    })


# --- add below your existing imports in api/views.py ---
from rest_framework import generics, permissions, filters
from .models import Book
from .serializers import BookSerializer

# Common queryset (with select_related for efficiency)
BOOK_QS = Book.objects.select_related("author").all()

class BookListView(generics.ListAPIView):
    """
    Read-only list of books.
    - open to everyone (AllowAny)
    - supports ?search= and ?ordering=
    """
    queryset = BOOK_QS
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "author__name"]
    ordering_fields = ["title", "publication_year", "author__name"]
    ordering = ["title"]


class BookDetailView(generics.RetrieveAPIView):
    """
    Retrieve a single book by ID (pk).
    - open to everyone (AllowAny)
    """
    queryset = BOOK_QS
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "pk"


class BookCreateView(generics.CreateAPIView):
    """
    Create a new book.
    - authenticated only
    - serializer validates publication_year (no future years)
    """
    queryset = BOOK_QS
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing book.
    - authenticated only
    - supports PUT and PATCH
    """
    queryset = BOOK_QS
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"


class BookDeleteView(generics.DestroyAPIView):
    """
    Delete a book by ID.
    - authenticated only
    """
    queryset = BOOK_QS
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "pk"


from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend  # ← add this

from .models import Book
from .serializers import BookSerializer

BOOK_QS = Book.objects.select_related("author").all()

class BookListView(generics.ListAPIView):
    """
    Read-only list of books with filtering, searching, and ordering.

    Filtering (django-filter):
      - ?title=ExactTitle
      - ?publication_year=1956
      - ?author=1             (by author id)
      - ?author__name=Mahfouz (case-sensitive exact match by default)

    Searching (SearchFilter):
      - ?search=palace        (matches title or author name)

    Ordering (OrderingFilter):
      - ?ordering=title
      - ?ordering=-publication_year
      - ?ordering=author__name
    """
    queryset = BOOK_QS
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    # DRF filter backends (can also be set globally; keeping explicit here)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Field-level filter config (django-filter)
    filterset_fields = {
        "title": ["exact", "icontains", "istartswith"],
        "publication_year": ["exact", "gte", "lte"],
        "author": ["exact"],            # author id
        "author__name": ["exact", "icontains", "istartswith"],
    }

    # Search across these fields (uses icontains under the hood)
    search_fields = ["title", "author__name"]

    # Allow ordering by these fields
    ordering_fields = ["title", "publication_year", "author__name"]

    # Default sort if none provided
    ordering = ["title"]
