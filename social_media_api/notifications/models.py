from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()

class Notification(models.Model):
    recipient = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.CASCADE
    )
    actor = models.ForeignKey(
        User,
        related_name='notifications_from',
        on_delete=models.CASCADE
    )
    verb = models.CharField(max_length=255)  # e.g., "liked your post", "followed you"

    # Generic relation (can point to Post, Comment, etc.)
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    target_object_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    # ✅ Add the timestamp (the field you’re missing)
    timestamp = models.DateTimeField(auto_now_add=True)

    # Whether the notification has been read
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target or ''} → {self.recipient}"
