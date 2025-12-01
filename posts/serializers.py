from rest_framework import serializers
from .models import Post, PostFile, PostComment, Like


    
class PostFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFile
        fields = ['id', 'file', 'created_at']
        extra_kwargs = {
            'post': {'read_only': True}
        }


class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    files = PostFileSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['user', 'id','username','first_name', 'caption', 'is_active', 'is_public', 'created_at', 'files']
        extra_kwargs = {
            'user': {'read_only': True}
        }
        
    def get_username(self, obj):
        return obj.user.username
    
    def get_first_name(self, obj):
        return obj.user.first_name
    
    
class PostCommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = PostComment
        fields = ['id','username','post', 'user', 'text']
        extra_kwargs = {
            'post': {'read_only': True},
            'user': {'read_only': True},
        }

    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        else:
            return None
    
    
class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post', 'user', 'is_liked']
        extra_kwargs = {
            'post': {'read_only': True},
            'user': {'read_only': True},
            'is_liked': {'required': False},
        }
    