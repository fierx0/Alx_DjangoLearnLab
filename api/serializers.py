from datetime import date
from rest_framework import serializers
from .models import Author, Book

# ----------------------------------------------------------
# BookSerializer
# ----------------------------------------------------------
# Serializes all fields of Book and validates publication_year
# to ensure it is not set in the future.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "publication_year", "author"]
        read_only_fields = ["id"]

    def validate_publication_year(self, value: int) -> int:
        """
        Ensure the publication_year is not in the future.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"publication_year cannot be in the future (>{current_year})."
            )
        return value


# ----------------------------------------------------------
# AuthorSerializer (nested)
# ----------------------------------------------------------
# Includes the author's name and a nested list of related books.
# We support:
#  - READ: shows nested BookSerializer (author.books)
#  - WRITE: allows creating/updating the author together with nested books
#
# How the relationship is handled:
#  - Author has related_name='books' on Book.author
#  - The nested 'books' field maps to that reverse relation
#  - We override create/update to write nested data explicitly
class AuthorSerializer(serializers.ModelSerializer):
    # Nested serializer. We allow writes, so no read_only=True here.
    books = BookSerializer(many=True)

    class Meta:
        model = Author
        fields = ["id", "name", "books"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """
        Create Author and (optionally) nested Books in one request.
        """
        books_data = validated_data.pop("books", [])
        author = Author.objects.create(**validated_data)
        for b in books_data:
            # Each `b` is validated by BookSerializer (including year check)
            Book.objects.create(author=author, **b)
        return author

    def update(self, instance, validated_data):
        """
        Update Author and replace its nested Books.
        Strategy shown here: full replace of the books collection.
        You could implement a more surgical upsert if you prefer.
        """
        books_data = validated_data.pop("books", None)

        # Update scalar fields on Author
        instance.name = validated_data.get("name", instance.name)
        instance.save()

        # If books were provided, replace existing set
        if books_data is not None:
            instance.books.all().delete()
            for b in books_data:
                Book.objects.create(author=instance, **b)

        return instance

    def validate(self, attrs):
        """
        Optional: enforce any author-level constraints that may
        involve nested books (e.g., uniqueness of titles per author).
        Here we keep it simple; the BookSerializer already validates years.
        """
        return attrs
