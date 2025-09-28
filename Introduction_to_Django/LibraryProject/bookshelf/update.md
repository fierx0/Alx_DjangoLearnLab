# UPDATE the Book's title

**Shell command:**
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984", author="George Orwell", publication_year=1949)
book.title = "Nineteen Eighty-Four"
book.save()
(book.id, book.title, book.author, book.publication_year)
