from rest_framework import viewsets, filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Category, Supplier, Product, Stock, Movement
from .serializers import CategorySerializer, SupplierSerializer, ProductSerializer, MovementSerializer
from .permissions import ReadOnlyOrAuthenticatedWrite


# ---------------------------
# Base CRUD ViewSets
# ---------------------------
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


# ---------------------------
# Inventory Movement Endpoints
# ---------------------------

def apply_stock_movement(product, movement_type, quantity):
    """Helper to apply stock updates safely."""
    stock, _ = Stock.objects.get_or_create(product=product)
    if movement_type == "RECEIVE":
        stock.on_hand += quantity
    elif movement_type == "ISSUE":
        if stock.on_hand < quantity:
            raise ValueError("Insufficient stock to issue")
        stock.on_hand -= quantity
    elif movement_type == "ADJUST":
        stock.on_hand = max(0, stock.on_hand + quantity)
    stock.save()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def receive_stock(request):
    product_id = request.data.get("product")
    qty = int(request.data.get("quantity", 0))
    reason = request.data.get("reason", "")

    try:
        product = Product.objects.get(id=product_id)
        apply_stock_movement(product, "RECEIVE", qty)
        movement = Movement.objects.create(
            product=product,
            movement_type="RECEIVE",
            quantity=qty,
            reason=reason,
            created_by=request.user,
        )
        serializer = MovementSerializer(movement)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def issue_stock(request):
    product_id = request.data.get("product")
    qty = int(request.data.get("quantity", 0))
    reason = request.data.get("reason", "")

    try:
        product = Product.objects.get(id=product_id)
        apply_stock_movement(product, "ISSUE", qty)
        movement = Movement.objects.create(
            product=product,
            movement_type="ISSUE",
            quantity=qty,
            reason=reason,
            created_by=request.user,
        )
        serializer = MovementSerializer(movement)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def adjust_stock(request):
    product_id = request.data.get("product")
    qty = int(request.data.get("quantity", 0))
    reason = request.data.get("reason", "")

    try:
        product = Product.objects.get(id=product_id)
        apply_stock_movement(product, "ADJUST", qty)
        movement = Movement.objects.create(
            product=product,
            movement_type="ADJUST",
            quantity=qty,
            reason=reason,
            created_by=request.user,
        )
        serializer = MovementSerializer(movement)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def low_stock_report(request):
    """List products where stock < 5 units."""
    low_stocks = Stock.objects.filter(on_hand__lt=5)
    data = [
        {
            "product": s.product.name,
            "sku": s.product.sku,
            "on_hand": s.on_hand,
        }
        for s in low_stocks
    ]
    return Response(data)
