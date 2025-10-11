# notifications/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()

class ActorMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class NotificationSerializer(serializers.ModelSerializer):
    actor = ActorMiniSerializer(read_only=True)
    target_repr = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            'id', 'actor', 'verb', 'target_repr',
            'is_read', 'created_at'
        )

    def get_target_repr(self, obj):
        t = obj.target
        if t is None:
            return None
        # minimal useful representation
        if hasattr(t, 'title'):
            return getattr(t, 'title')
        return str(t)
