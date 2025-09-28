# Advanced API Project — DRF Generic Views

## Endpoints
- `GET /api/books/` — list (AllowAny). Supports `?search=` and `?ordering=`.
- `GET /api/books/<pk>/` — retrieve (AllowAny).
- `POST /api/books/create/` — create (IsAuthenticated).
- `PUT/PATCH /api/books/<pk>/update/` — update (IsAuthenticated).
- `DELETE /api/books/<pk>/delete/` — delete (IsAuthenticated).

## Permissions
Read-only for anonymous, write operations require authentication.

## Implementation Notes
- Views use DRF generics (`ListAPIView`, `RetrieveAPIView`, `CreateAPIView`, `UpdateAPIView`, `DestroyAPIView`).
- Search/ordering enabled via `SearchFilter` and `OrderingFilter`.
- `BookSerializer` validates `publication_year` to not exceed the current year.


## Filtering / Searching / Ordering

### Filtering (django-filter)
- `GET /api/books/?title=ExactTitle`
- `GET /api/books/?title__icontains=palace`
- `GET /api/books/?publication_year=1956`
- `GET /api/books/?publication_year__gte=1950&publication_year__lte=1960`
- `GET /api/books/?author=1` (by author id)
- `GET /api/books/?author__name=Mahfouz`

### Search (SearchFilter)
- `GET /api/books/?search=palace` (matches title or author name)

### Ordering (OrderingFilter)
- `GET /api/books/?ordering=title`
- `GET /api/books/?ordering=-publication_year`
- `GET /api/books/?ordering=author__name`
