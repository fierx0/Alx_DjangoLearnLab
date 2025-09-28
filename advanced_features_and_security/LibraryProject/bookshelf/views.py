from django.shortcuts import render

# Create your views here.
# advanced_features_and_security/core/views.py
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Article

# ---------- FBV examples ----------
@login_required
@permission_required('core.can_view', raise_exception=True)
def article_list(request):
    qs = Article.objects.select_related("author").order_by("-created_at")
    return render(request, "core/article_list.html", {"book_list", "books": qs})

@login_required
@permission_required('core.can_view', raise_exception=True)
def article_detail(request, pk):
    obj = get_object_or_404(Article, pk=pk)
    return render(request, "core/article_detail.html", {"article": obj})

@login_required
@permission_required('core.can_create', raise_exception=True)
def article_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        body = request.POST.get("body")
        Article.objects.create(title=title, body=body, author=request.user)
        return redirect("core:article_list")
    return render(request, "core/article_form.html")

@login_required
@permission_required('core.can_edit', raise_exception=True)
def article_edit(request, pk):
    obj = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        obj.title = request.POST.get("title")
        obj.body = request.POST.get("body")
        obj.save()
        return redirect("core:article_detail", pk=obj.pk)
    return render(request, "core/article_form.html", {"article": obj})

@login_required
@permission_required('core.can_delete', raise_exception=True)
def article_delete(request, pk):
    obj = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        obj.delete()
        return redirect("core:article_list")
    return render(request, "core/article_confirm_delete.html", {"article": obj})

# ---------- CBV examples ----------
class ArticleListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Article
    template_name = "core/article_list.html"
    context_object_name = "articles"
    ordering = ["-created_at"]
    permission_required = "core.can_view"
    raise_exception = True

class ArticleDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Article
    template_name = "core/article_detail.html"
    context_object_name = "article"
    permission_required = "core.can_view"
    raise_exception = True

class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Article
    fields = ["title", "body"]
    template_name = "core/article_form.html"
    success_url = reverse_lazy("core:article_list")
    permission_required = "core.can_create"
    raise_exception = True

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Article
    fields = ["title", "body"]
    template_name = "core/article_form.html"
    permission_required = "core.can_edit"
    raise_exception = True

class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Article
    template_name = "core/article_confirm_delete.html"
    success_url = reverse_lazy("core:article_list")
    permission_required = "core.can_delete"
    raise_exception = True


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Book
from .forms import BookSearchForm
from django.db.models import Q

@require_http_methods(["GET"])
def book_list(request):
    # Validate query via Django Form to avoid unsafe patterns
    form = BookSearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            # ORM lookups are parameterized and safe
            books = books.filter(
                Q(title__icontains=q) |
                Q(author__icontains=q)
            )

    return render(request, "bookshelf/book_list.html", {"books": books, "form": form})

@login_required
@require_http_methods(["GET", "POST"])
def book_create(request):
    from django import forms

    class BookForm(forms.ModelForm):
        class Meta:
            model = Book
            fields = ["title", "author", "publication_year"]

    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():          # validates & sanitizes user input
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()

    return render(request, "bookshelf/form_example.html", {"form": form})

@require_http_methods(["GET"])
def book_detail(request, pk):
    # Always use ORM or parameterized queries; never format SQL strings with user input.
    book = get_object_or_404(Book, pk=pk)
    return render(request, "bookshelf/book_detail.html", {"book": book})


# If you ever MUST use raw SQL, parameterize properly:
from django.db import connection

def safe_raw_example(title_prefix: str):
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT id, title FROM bookshelf_book WHERE title LIKE %s",
            [f"{title_prefix}%"]
        )
        rows = cursor.fetchall()
    return rows
"from .forms import ExampleForm"