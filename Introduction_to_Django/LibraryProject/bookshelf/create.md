# CREATE a Book

**Shell command:**
```python
from bookshelf.models import Book
b = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
b.id  # show PK to confirm it saved
b     # show __str__ representation
