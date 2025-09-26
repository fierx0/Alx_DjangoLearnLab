from rest_framework import serializers
from .models import Category, Supplier, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    supplier_name = serializers.CharField(source="default_supplier.name", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "sku", "name", "category", "category_name",
            "unit", "default_supplier", "supplier_name",
            "is_active", "created_at", "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    # Optional example of lightweight validation
    def validate_sku(self, value):
        if " " in value:
            raise serializers.ValidationError("SKU must not contain spaces.")
        return value.upper()  # normalize
