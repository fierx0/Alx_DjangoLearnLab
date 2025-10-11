# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Users this user follows
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        through='Follow',
        related_name='followers',
        blank=True,
    )

class Follow(models.Model):
    follower = models.ForeignKey('User', on_delete=models.CASCADE, related_name='following_relations')
    following = models.ForeignKey('User', on_delete=models.CASCADE, related_name='follower_relations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('follower', 'following'),)
        indexes = [
            models.Index(fields=['follower', 'following']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'{self.follower.username} → {self.following.username}'
