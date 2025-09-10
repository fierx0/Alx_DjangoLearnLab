# accounts/managers.py
from django.contrib.auth.models import UserManager as DjangoUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class UserManager(DjangoUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError(_("The given username must be set"))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        if extra_fields.get("date_of_birth") is not None:
            # Optionally validate DOB logic here (e.g., must be in the past)
            pass
        user.set_password(password)
        user.full_clean(exclude=["password"])  # validate model fields except hashed password
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValidationError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValidationError(_("Superuser must have is_superuser=True."))

        return self._create_user(username, email, password, **extra_fields)
