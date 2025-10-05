from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile, Post, Comment, Tag

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
    tags_csv = forms.CharField(required=False, help_text="Comma-separated (e.g. python, django)")
    class Meta:
        model = Post
        fields = ("title", "content", "tags")  # tags handled via tags_csv
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            names = [t.name for t in self.instance.tags.all()]
            self.fields["tags_csv"].initial = ", ".join(names)
            widgets = {
            "tags": TagWidget(),      # ✅ use Taggit’s TagWidget
        }
    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Title cannot be empty.")
        return title
    def parsed_tags(self):
        raw = self.cleaned_data.get("tags_csv", "")
        parts = [p.strip() for p in raw.split(",") if p.strip()]
        # normalize to lowercase & keep order without dups
        return list(dict.fromkeys([p.lower() for p in parts]))

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
