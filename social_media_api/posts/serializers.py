# posts/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()

class AuthorMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorMiniSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'created_at', 'updated_at')
        read_only_fields = ('id', 'author', 'created_at', 'updated_at')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        comment = super().create(validated_data)

        # notify post author (if not self)
        try:
            from notifications.models import Notification
            if comment.post.author_id != request.user.id:
                Notification.objects.create(
                    recipient=comment.post.author,
                    actor=request.user,
                    verb='commented',
                    target=comment.post  # generic target
                )
        except Exception:
            pass  # keep API resilient even if notifications fail

        return comment

class PostSerializer(serializers.ModelSerializer):
    author = AuthorMiniSerializer(read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'id', 'author', 'title', 'content',
            'created_at', 'updated_at',
            'comments_count', 'likes_count', 'is_liked'
        )
        read_only_fields = (
            'id', 'author', 'created_at', 'updated_at',
            'comments_count', 'likes_count', 'is_liked'
        )

    def get_is_liked(self, obj):
        request = self.context.get('request')
        if not request or not request.user or not request.user.is_authenticated:
            return False
        return Like.objects.filter(post=obj, user=request.user).exists()

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)
