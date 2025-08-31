# DELETE the Book and confirm removal

**Shell command:**
```python
from bookshelf.models import Book
deleted_count, _ = Book.objects.filter(author="George Orwell", publication_year=1949).delete()
deleted_count
list(Book.objects.all())
