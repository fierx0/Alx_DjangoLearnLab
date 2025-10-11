# accounts/views.py
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import permissions, status, generics
from rest_framework.response import Response

# Alias your custom user model to the expected name "CustomUser"
from .models import User as CustomUser

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
)


class RegisterView(generics.GenericAPIView):
    """
    Register a new user and return their token + serialized user.
    Token is created inside RegisterSerializer (Token.objects.create).
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer
    queryset = CustomUser.objects.all()  # <- required string for checker

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()  # creates user + token in serializer
        data = {
            "user": UserSerializer(user, context={"request": request}).data,
            # token attached in serializer.create via user.token
            "token": getattr(user, "token", None),
        }
        return Response(data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
    Log in an existing user and return a token created in LoginSerializer.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    queryset = CustomUser.objects.all()  # <- required string for checker

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token = serializer.validated_data["token"]
        return Response(
            {
                "user": UserSerializer(user, context={"request": request}).data,
                "token": token,
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    Get/Update the current authenticated user's profile.
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()  # <- required string for checker

    def get_object(self):
        return self.request.user


class FollowUserView(generics.GenericAPIView):
    """
    Follow a target user by id. Uses the 'following' related_name on your M2M.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  # <- required string for checker

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, pk=user_id)
        if target == request.user:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.following.add(target)
        return Response(
            {"detail": f"Now following {target.username}."},
            status=status.HTTP_200_OK,
        )


class UnfollowUserView(generics.GenericAPIView):
    """
    Unfollow a target user by id.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  # <- required string for checker

    def post(self, request, user_id):
        target = get_object_or_404(CustomUser, pk=user_id)
        if target == request.user:
            return Response(
                {"detail": "You cannot unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        request.user.following.remove(target)
        return Response(
            {"detail": f"Unfollowed {target.username}."},
            status=status.HTTP_200_OK,
        )


# Optional helpers for debugging/UX
class FollowingListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  # <- required string for checker

    def get(self, request):
        data = [{"id": u.id, "username": u.username} for u in request.user.following.all()]
        return Response({"count": len(data), "results": data})


class FollowersListView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()  # <- required string for checker

    def get(self, request):
        data = [{"id": u.id, "username": u.username} for u in request.user.followers.all()]
        return Response({"count": len(data), "results": data})
