from rest_framework import serializers
from .models import *

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):
    content_url = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ["id",'username','caption','content_url']
    
    def get_username(self, obj):
        return obj.user.username
    
    def get_content_url(self,obj):
        return f"http://127.0.0.1:8000/posts/{obj.id}/media"
    

class StroySerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    class Meta:
        model = ProfileStory
        fields = ["type","video","image","created_at","url"]

    def get_url(self, obj):
        return f"http://127.0.0.1:8000/posts/story/{obj.user.id}/{obj.id}"

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    like_url = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ['user','username','post','content','likes','like_url']
        read_only_fields = ['user','post']
    def get_username(self, obj):
        return obj.user.username
    
    def get_likes(self, obj):
        try:
            return obj.likes_count()
        except:
            return 0
    def get_like_url(self, obj):
        return f"http://127.0.0.1:8000/posts/comments/{obj.id}/like"