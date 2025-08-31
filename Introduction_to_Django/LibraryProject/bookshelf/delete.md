# DELETE the Book and confirm removal

**Shell command:**
```python
from bookshelf.models import Book
# Since the title was updated earlier, target the updated record:
book = Book.objects.get(title="Nineteen Eighty-Four", author="George Orwell", publication_year=1949)
deleted_info = book.delete()  # <- REQUIRED: instance delete
deleted_info
list(Book.objects.all())

