
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from frienship.serializers import UserListSerializer 
from django.contrib.auth.models import User
from rest_framework import status
from .models import Friendship
from django.db.models import Q
#user list
class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            users = User.objects.filter(is_superuser=False, is_staff=False,is_active=True)
            serializer = UserListSerializer(users, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
#friend-requests/<int:pk>
class FriendRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            friend = User.objects.get(pk=pk)
            if friend == request.user:
                return Response({'error': 'You cannot send a friend request to yourself'}, status=status.HTTP_400_BAD_REQUEST)
            if Friendship.objects.filter(sender=request.user, receiver=friend).exists():
                return Response({'error': 'You have already sent a friend request to this user'}, status=status.HTTP_400_BAD_REQUEST)
            if Friendship.objects.filter(sender=friend, receiver=request.user).exists():
                return Response({'error': 'This user has already sent you a friend request'}, status=status.HTTP_400_BAD_REQUEST)
            friendship = Friendship.objects.create(sender=request.user, receiver=friend, status='pending')
            return Response({'message': 'Friend request sent'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
#friend-requests-list/
class FriendRequestListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            friendships = Friendship.objects.filter(receiver=request.user, status='pending')
            users = [fr.sender for fr in friendships]
            serializer = UserListSerializer(users, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
#friend-requests/<int:pk>/accept/
class FriendRequestAcceptView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            friendship = Friendship.objects.get(sender=user, receiver=request.user, status='pending')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        friendship.status = 'accepted'
        friendship.save()
        return Response({'message': 'Friend request accepted'})
    
#friend-requests/<int:pk>/reject/
class FriendRequestRejectView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            friendship = Friendship.objects.get(sender=user, receiver=request.user, status='pending')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        friendship.status = 'rejected'
        friendship.save()
        return Response({'message': 'Friend request rejected'})
    
#friend-requests/
class FriendRequestListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            friendships = Friendship.objects.filter(
                Q(receiver=request.user, status='accepted') | Q(sender=request.user, status='accepted'))
            print(friendships.query)
            
            users = [fr.sender for fr in friendships]
            serializer = UserListSerializer(users, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
