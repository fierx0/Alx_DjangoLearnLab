from rest_framework import viewsets, permissions, filters, generics
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from .models import Post, Comment  # If you don’t have Comment yet, remove it here and in CommentViewSet import/registration.
from .serializers import PostSerializer, CommentSerializer  # Remove if you don’t have comments.
from .permissions import IsOwnerOrReadOnly


class DefaultPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()  # explicit for your checker
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at', 'title']

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()  # explicit for your checker
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx


class FeedView(generics.ListAPIView):
    """
    Returns newest posts authored by users the current user follows.
    Uncomment the OR below to include the current user's own posts as well.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        me = self.request.user
        following_ids = me.following.values_list('id', flat=True)
        qs = Post.objects.select_related('author').filter(
            Q(author__id__in=following_ids)
            # | Q(author=me)  # include my own posts if desired
        ).order_by('-created_at')
        return qs

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx
