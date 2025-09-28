from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
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
