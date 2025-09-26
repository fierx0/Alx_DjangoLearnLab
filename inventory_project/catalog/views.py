from rest_framework import viewsets, filters
from .models import Category, Supplier, Product
from .serializers import CategorySerializer, SupplierSerializer, ProductSerializer
from .permissions import ReadOnlyOrAuthenticatedWrite


class BaseViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnlyOrAuthenticatedWrite]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]


class CategoryViewSet(BaseViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer


class SupplierViewSet(BaseViewSet):
    queryset = Supplier.objects.all().order_by("name")
    serializer_class = SupplierSerializer
    search_fields = ["name", "contact_email", "phone"]


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.select_related("category", "default_supplier").all().order_by("name")
    serializer_class = ProductSerializer
    search_fields = ["name", "sku"]
