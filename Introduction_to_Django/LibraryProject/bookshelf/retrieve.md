# RETRIEVE the created Book

**Shell command:**
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984", author="George Orwell", publication_year=1949)
(book.id, book.title, book.author, book.publication_year)
