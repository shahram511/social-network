from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics
from django.contrib.auth import get_user_model

from accounts.serializers import RegisterSerializer

# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
        