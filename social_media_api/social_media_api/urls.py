"""
URL configuration for social_media_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

urlpatterns = [
    # Django admin site
    path('admin/', admin.site.urls),

    # Accounts app (register, login, profile, follow/unfollow)
    path('api/accounts/', include('accounts.urls')),

    # Posts app (CRUD, comments, likes, feed)
    path('api/', include('posts.urls')),

    # Notifications app
    path('api/notifications/', include('notifications.urls')),

    # Optional: root route to display API overview
    path('', lambda request: JsonResponse({
        "message": "Welcome to the Social Media API 🚀",
        "available_routes": {
            "accounts": {
                "register": "/api/accounts/register/",
                "login": "/api/accounts/login/",
                "profile": "/api/accounts/profile/",
                "follow": "/api/accounts/follow/<user_id>/",
                "unfollow": "/api/accounts/unfollow/<user_id>/",
                "following": "/api/accounts/following/",
                "followers": "/api/accounts/followers/"
            },
            "posts": {
                "list_create": "/api/posts/",
                "retrieve_update_delete": "/api/posts/<id>/",
                "comments": "/api/comments/",
                "feed": "/api/feed/",
                "like": "/api/posts/<id>/like/",
                "unlike": "/api/posts/<id>/unlike/"
            },
            "notifications": {
                "list": "/api/notifications/",
                "mark_read": "/api/notifications/<id>/read/",
                "mark_all_read": "/api/notifications/read-all/"
            },
            "admin": "/admin/"
        }
    })),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
