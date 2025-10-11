from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

User = get_user_model()


class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, pk=user_id)
        if target == request.user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.add(target)
        return Response({"detail": f"Now following {target.username}."}, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target = get_object_or_404(User, pk=user_id)
        if target == request.user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.following.remove(target)
        return Response({"detail": f"Unfollowed {target.username}."}, status=status.HTTP_200_OK)


# Optional helper endpoints (nice for debugging/UX)
class FollowingListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = [{"id": u.id, "username": u.username} for u in request.user.following.all()]
        return Response({"count": len(data), "results": data})


class FollowersListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = [{"id": u.id, "username": u.username} for u in request.user.followers.all()]
        return Response({"count": len(data), "results": data})
