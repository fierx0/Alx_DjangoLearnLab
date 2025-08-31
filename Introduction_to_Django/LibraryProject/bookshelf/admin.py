
from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns shown in the changelist (table)
    list_display = ("id", "title", "author", "publication_year")
    list_display_links = ("title",)
    ordering = ("title",)  # default sort
    list_per_page = 25
    save_on_top = True

    # Right-side filters
    list_filter = ("publication_year", "author")

    # Top search box
    search_fields = ("title", "author")

# Optional: brand the admin site a bit
admin.site.site_header = "Library Admin"
admin.site.site_title = "Library Admin"
admin.site.index_title = "Library Management"
