from django.contrib import admin
from .models import Category, Supplier, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "contact_email", "phone")
    search_fields = ("name", "contact_email", "phone")
    ordering = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "sku", "name", "category", "default_supplier", "unit", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("sku", "name")
    autocomplete_fields = ("category", "default_supplier")
    ordering = ("name",)
