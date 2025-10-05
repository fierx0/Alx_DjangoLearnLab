
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .forms import RegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import Post

def post_list(request):
    posts = Post.objects.select_related("author")
    return render(request, "blog/post_list.html", {"posts": posts})

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

@login_required
def profile(request):
    return render(request, "blog/profile.html")

@login_required
def profile_edit(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profile updated.")
            return redirect("blog:profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, "blog/profile_edit.html", {"u_form": u_form, "p_form": p_form})
