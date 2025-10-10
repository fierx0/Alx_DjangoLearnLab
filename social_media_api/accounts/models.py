# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    followers = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=False,
        related_name='following'
    )

    def followers_count(self) -> int:
        return self.followers.count()

    def following_count(self) -> int:
        return self.following.count()

    def __str__(self):
        return self.username
