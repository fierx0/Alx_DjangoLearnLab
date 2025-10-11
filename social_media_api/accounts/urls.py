from django.urls import path
from .views import (
    FollowUserView, UnfollowUserView,
    FollowingListView, FollowersListView,
)

# keep your existing routes for register/login/profile
urlpatterns = [
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    path('following/', FollowingListView.as_view(), name='following-list'),  # optional
    path('followers/', FollowersListView.as_view(), name='followers-list'),  # optional
]
