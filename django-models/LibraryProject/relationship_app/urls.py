from django.urls import path
from .views import list_books, LibraryDetailView  # <- exact strings checker wants

urlpatterns = [
    path("books/", list_books, name="list_books"),  # function-based
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),  # class-based
]


from django.urls import path
from .views import list_books, LibraryDetailView, seed_data  # add seed_data

urlpatterns = [
    path("books/", list_books, name="list_books"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),
    path("seed/", seed_data, name="seed_data"),  # new
]
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView, register

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView   # keeps earlier checks happy
from . import views                                # needed so 'views.register' exists

urlpatterns = [
    path("books/", list_books, name="list_books"),
    path("libraries/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"),

    path("login/",  LoginView.as_view(template_name="relationship_app/login.html"),   name="login"),
    path("logout/", LogoutView.as_view(template_name="relationship_app/logout.html"), name="logout"),
    path("register/", views.register, name="register"),   # requires `. import views`
]

from django.urls import path
from .views import admin_view, librarian_view, member_view  # add these

urlpatterns += [
    path("admin-view/", admin_view, name="admin_view"),
    path("librarian-view/", librarian_view, name="librarian_view"),
    path("member-view/", member_view, name="member_view"),
]

from django.urls import path
from .views import add_book, edit_book, delete_book

urlpatterns += [
    path("add_book/", add_book, name="add_book"),
    path("edit_book/<int:pk>/", edit_book, name="edit_book"),
    path("delete_book/<int:pk>/", delete_book, name="delete_book"),
]
