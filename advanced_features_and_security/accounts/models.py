from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import UserManager

def user_profile_upload_to(instance, filename):
    # e.g., users/42/profile_photo.png
    return f"users/{instance.pk or 'new'}/profile/{filename}"

class User(AbstractUser):
    date_of_birth = models.DateField(_("date of birth"), null=True, blank=True)
    profile_photo = models.ImageField(
        _("profile photo"),
        upload_to=user_profile_upload_to,
        null=True,
        blank=True,
    )

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.get_username()

# in any app e.g., core/models.py
from django.conf import settings
from django.db import models

class Article(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )
    # ...
