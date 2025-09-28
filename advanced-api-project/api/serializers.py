from datetime import date
from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """Serialize Book and validate that publication_year is not in the future."""
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]
        read_only_fields = ["id"]

    def validate_publication_year(self, value: int) -> int:
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"publication_year cannot be in the future (>{current_year})."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Read-only nested books list for an author.
    The related_name='books' on Book.author powers this reverse relation.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
        read_only_fields = ["id"]
