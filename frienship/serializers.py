from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Friendship
from django.conf import settings

class UserListSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']
        
    def get_avatar(self, obj):
        """Return full URL for user's avatar"""
        try:
            if hasattr(obj, 'profile') and obj.profile and obj.profile.avatar:
                avatar_url = obj.profile.avatar.url
                # Return full URL using request context
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(avatar_url)
                # Fallback using BASE_URL from settings
                base_url = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000/')
                return f"{base_url.rstrip('/')}{avatar_url}"
        except AttributeError:
            pass
        except Exception:
            pass
        return None
        
# class FriendRequestSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Friendship
#         fields = ['id', 'sender', 'receiver']