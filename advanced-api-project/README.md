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
