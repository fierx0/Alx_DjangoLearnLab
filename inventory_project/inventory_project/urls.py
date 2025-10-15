"""
URL configuration for inventory_project project.
"""

from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.http import HttpResponse
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from catalog.views import CategoryViewSet, SupplierViewSet, ProductViewSet
from catalog import views as catalog_views


# Router for CRUD endpoints
router = DefaultRouter()
router.register(r'catalog/categories', CategoryViewSet, basename='category')
router.register(r'catalog/suppliers', SupplierViewSet, basename='supplier')
router.register(r'catalog/products', ProductViewSet, basename='product')


# Simple health check endpoint
def health(_request):
    return HttpResponse("ok")


urlpatterns = [
    # Redirect root "/" → "/api/"
    path("", RedirectView.as_view(url="/api/", permanent=False)),

    # Admin
    path("admin/", admin.site.urls),

    # API routes (CRUD)
    path("api/", include(router.urls)),

    # Auth (token)
    path("api/auth/token/", obtain_auth_token),

    # Inventory endpoints
    path("api/inventory/receive/", catalog_views.receive_stock),
    path("api/inventory/issue/", catalog_views.issue_stock),
    path("api/inventory/adjust/", catalog_views.adjust_stock),
    path("api/inventory/reorder/low-stock/", catalog_views.low_stock_report),

    # API Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # Health endpoint
    path("api/health/", health),
]
