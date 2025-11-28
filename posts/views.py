from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Post, PostFile, PostComment, Like

from .serializers import PostSerializer, PostFileSerializer, PostCommentSerializer, LikeSerializer

from django.db import models


class PostView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    def get(self, request, post_pk):    
        try:
            post = Post.objects.get(pk=post_pk,user=request.user)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
    def post(self, request):
        # print(request.user)
        # print(request.auth)
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class PostListView(APIView):
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
class PostFileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, post_pk, file_pk):
        try:
            post = Post.objects.get(pk=post_pk,user=request.user)
            file = post.files.get(pk=file_pk)
        except (Post.DoesNotExist, PostFile.DoesNotExist):
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostFileSerializer(file)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, post_pk):
        """upload file to post"""
        try:
            post = Post.objects.get(pk=post_pk,user=request.user)
        except Post.DoesNotExist:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostFileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class PostCommentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_post(self, request, post_pk):
        try:
            post = Post.objects.get(pk=post_pk)
            return post
        except Post.DoesNotExist:
            return False
        
    
    def get(self, request, post_pk):
        post = self.get_post(request, post_pk)
        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        comments = post.comments.filter(models.Q(is_approved=True) | models.Q(user=request.user))
        serializer = PostCommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, post_pk):
        post = self.get_post(request, post_pk)
        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_post(self, request, post_pk):
        try:
            post = Post.objects.get(pk=post_pk)
            return post
        except Post.DoesNotExist:
            return False
        
    def get(self, request, post_pk):
        post = self.get_post(request, post_pk)
        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        likes = post.likes.filter(is_liked=True).count()
        return Response({"likes": likes}, status=status.HTTP_200_OK)
    
    def post(self, request, post_pk):
        post = self.get_post(request, post_pk)
        if not post:
            return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = LikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        