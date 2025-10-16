"""
URL configuration for inventory_project project.
"""

from django.contrib import admin
from django.urls import path, include
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


# Simple homepage 
def home(_request):
    return HttpResponse("""
        <html>
            <head>
                <title>Inventory Management API</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        margin: 40px;
                        background-color: #f9f9f9;
                        color: #333;
                    }
                    h1 {
                        color: #2c3e50;
                    }
                    .container {
                        max-width: 800px;
                        margin: auto;
                        background: white;
                        padding: 30px;
                        border-radius: 12px;
                        box-shadow: 0 0 10px rgba(0,0,0,0.1);
                    }
                    a {
                        display: inline-block;
                        margin: 8px 0;
                        color: #007BFF;
                        text-decoration: none;
                        font-weight: bold;
                    }
                    a:hover {
                        text-decoration: underline;
                    }
                    p {
                        line-height: 1.6;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Welcome to the Inventory Management API</h1>
                    <p>This API allows you to manage products, suppliers, categories, and stock movements.</p>
                    <h3>Quick Links:</h3>
                    <ul>
                        <li><a href="/api/">API Root</a></li>
                        <li><a href="/api/docs/">Swagger Documentation</a></li>
                        <li><a href="/api/redoc/">ReDoc Documentation</a></li>
                        <li><a href="/admin/">Django Admin Panel</a></li>
                    </ul>
                    <p><small>Built with Django REST Framework — Capstone Project by Abdellah Idmhand</small></p>
                </div>
            </body>
        </html>
    """)


# Simple health check endpoint
def health(_request):
    return HttpResponse("ok")


urlpatterns = [
    # Homepage
    path("", home, name="home"),

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
]