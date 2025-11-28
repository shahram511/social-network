from django.urls import path

from .views import UserListAPIView, FriendRequestAPIView, FriendRequestAcceptView, FriendRequestListView, FriendRequestRejectView, FriendRequestListAPIView

urlpatterns = [
    path('users-list/', UserListAPIView.as_view(), name='users-list'),  #send friend request
    path('friend-requests/<int:pk>/', FriendRequestAPIView.as_view(), name='friend-request'), #send friend request
    path('friend-requests-list/', FriendRequestListView.as_view(), name='friend-request-list'), #get friend request list
    path('friend-requests/<int:pk>/accept/', FriendRequestAcceptView.as_view(), name='friend-request-accept'), #accept friend request
    path('friend-requests/<int:pk>/reject/', FriendRequestRejectView.as_view(), name='friend-request-reject'), #reject friend request
    # path('friend-requests/<int:pk>/', FriendRequestDetailView.as_view(), name='friend-request-detail'), #get friend request detail
    path('friend-requests/', FriendRequestListAPIView.as_view(), name='friend-request-list-api'), #get friend request list
]

