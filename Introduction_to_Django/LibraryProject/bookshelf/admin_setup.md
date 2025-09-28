# Django Admin setup for `bookshelf.Book`

## Files touched
- `bookshelf/admin.py` — registers `Book` with custom admin
- `LibraryProject/settings.py` — ensures `bookshelf` is in `INSTALLED_APPS`

## Admin config highlights
- `list_display = ("id", "title", "author", "publication_year")`
- `list_filter = ("publication_year", "author")`
- `search_fields = ("title", "author")`
- `ordering = ("title",)`
- Branding via `admin.site.site_header`, etc.

## How to use
1. `python manage.py createsuperuser`
2. `python manage.py runserver`
3. Go to `http://127.0.0.1:8000/admin/`
4. Manage **Book** entries (add, edit, delete), filter by year/author, and search by title/author.
