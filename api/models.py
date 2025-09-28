from django.db import models

# -----------------------------------------------
# Models
# -----------------------------------------------
# Author and Book demonstrate a one-to-many relationship:
# One Author can have many Books (Author -> Book = 1:N).
# We keep the models simple and focus on relationships + serialization.

class Author(models.Model):
    """
    Represents a book author.
    Fields:
      - name: Human-readable name of the author.
    """
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    """
    Represents a book.
    Fields:
      - title: Title of the book.
      - publication_year: Year the book was published (validated in serializer).
      - author: FK to Author, establishing the 1:N relationship.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name='books',  # enables reverse relation: author.books.all()
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return f"{self.title} ({self.publication_year})"
