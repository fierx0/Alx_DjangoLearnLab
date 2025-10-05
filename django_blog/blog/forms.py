from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile, Post, Comment

User = get_user_model()

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio",)
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content")
    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        return title

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {"content": forms.Textarea(attrs={"rows": 3, "placeholder": "Write a comment…"})}
    def clean_content(self):
        text = self.cleaned_data["content"].strip()
        if not text:
            raise forms.ValidationError("Comment cannot be empty.")
        return text
