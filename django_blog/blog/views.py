from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post, Comment, Tag
from .forms import (
    RegistrationForm, UserUpdateForm, ProfileUpdateForm,
    PostForm, CommentForm,
)

# ---------- Public list & detail ----------
class PostListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/post_list.html"
    paginate_by = 10

class PostDetailView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post_detail.html"
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["comments"] = self.object.comments.select_related("author")
        ctx["comment_form"] = CommentForm()
        return ctx

# ---------- Post CRUD ----------
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    def form_valid(self, form):
        form.instance.author = self.request.user
        resp = super().form_valid(form)
        tag_names = form.parsed_tags()
        tags = [Tag.objects.get_or_create(name=name, defaults={"slug": slugify(name)})[0] for name in tag_names]
        self.object.tags.set(tags)
        messages.success(self.request, "Post created.")
        return resp

class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author_id == self.request.user.id

class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    def form_valid(self, form):
        resp = super().form_valid(form)
        tag_names = form.parsed_tags()
        tags = [Tag.objects.get_or_create(name=name, defaults={"slug": slugify(name)})[0] for name in tag_names]
        self.object.tags.set(tags)
        messages.success(self.request, "Post updated.")
        return resp

class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("blog:post_list")
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Post deleted.")
        return super().delete(request, *args, **kwargs)

# ---------- Comment CRUD ----------
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs["pk"])  # URL uses pk for post
        form.instance.post = post
        form.instance.author = self.request.user
        messages.success(self.request, "Comment posted.")
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.post_id}) + "#comments"

class CommentAuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object().author_id == self.request.user.id

class CommentUpdateView(LoginRequiredMixin, CommentAuthorRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"
    def form_valid(self, form):
        messages.success(self.request, "Comment updated.")
        return super().form_valid(form)
    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.post_id}) + "#comments"

class CommentDeleteView(LoginRequiredMixin, CommentAuthorRequiredMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Comment deleted.")
        return super().delete(request, *args, **kwargs)
    def get_success_url(self):
        return reverse("blog:post_detail", kwargs={"pk": self.object.post_id}) + "#comments"

# ---------- Tag & Search ----------
class PostByTagListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/post_list.html"
    paginate_by = 10
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs["slug"])
        return Post.objects.select_related("author").prefetch_related("tags").filter(tags=self.tag)
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["active_tag"] = self.tag
        return ctx

class PostSearchListView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/search_results.html"
    paginate_by = 10
    def get_queryset(self):
        q = self.request.GET.get("q", "").strip()
        self.query = q
        if not q:
            return Post.objects.none()
        return (
            Post.objects.select_related("author").prefetch_related("tags")
            .filter(Q(title__icontains=q) | Q(content__icontains=q) | Q(tags__name__icontains=q))
            .distinct()
        )
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.query
        return ctx

# ---------- Auth ----------
class LoginView(auth_views.LoginView):
    template_name = "blog/login.html"

class LogoutView(auth_views.LogoutView):
    template_name = "blog/logged_out.html"

class RegisterView(View):
    def get(self, request):
        return render(request, "blog/register.html", {"form": RegistrationForm()})
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created. Please sign in.")
            return redirect("blog:login")
        return render(request, "blog/register.html", {"form": form})

# ---------- Profile ----------
@login_required
def profile(request):
    return render(request, "blog/profile.html")

@login_required
def profile_edit(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save(); p_form.save()
            messages.success(request, "Profile updated.")
            return redirect("blog:profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, "blog/profile_edit.html", {"u_form": u_form, "p_form": p_form})
