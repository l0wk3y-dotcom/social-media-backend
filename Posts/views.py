from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
# Create your views here.
class UploadContent(generics.CreateAPIView):
    serializer_class = ContentSerializer
    queryset = Content.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request, post_id, *args, **kwargs):
        if not post_id:
            return Response({"message" : "post id was not provided"})
        try:
            post = Post.objects.get(id = post_id)
        except Post.DoesNotExist:
            return Response({"message" : "post id was not valid"}, status = status.HTTP_404_NOT_FOUND)
        
        serializer = ContentSerializer(data = request.data)
        if serializer.is_valid():
            content = serializer.save(post = post)
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def get(self, request, post_id, *args, **kwargs):
        try:
            post = Post.objects.get(id = post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        queryset = Content.objects.filter(post = post)
        serializer = ContentSerializer(queryset, many = True)
        return Response(serializer.data)
    

class PostListCreateAPIView(APIView):
    # Get list of posts for a specific user
    def get(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)  # Ensure the user exists
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        posts = Post.objects.filter(user=user)
        serializer = PostSerializer(posts, many=True, context = {'request':request})
        return Response(serializer.data)

    # Create a new post for a specific user
    def post(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id=user_id)  # Ensure the user exists
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Return created post
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update an existing post

    # Delete a specific post


class PostRetrieveDeleteUpdate(APIView):
    def get(self, request, post_id , *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        sz = PostSerializer(post, context = {'request':request})
        return Response(sz.data) 
    
    def delete(self, request, post_id, *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    
    def put(self, request, post_id, *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id)  # Ensure the post belongs to the user
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)  # Return updated post
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreateListStory(generics.ListCreateAPIView):
    serializer_class = StroySerializer
    queryset = ProfileStory.objects.all()

    def get(self, request, user_id, *args, **kwargs):
        qs = ProfileStory.objects.filter(user__id = user_id)
        sz = StroySerializer(qs, many = True)
        return Response(sz.data)
    
    def post(self, request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(id = user_id)
        except User.DoesNotExist:
            return Response({"error" : "User Does not Exist! "})
        
        sz = StroySerializer(data = request.data)
        if sz.is_valid():
            sz.save(user = user)
            return Response(sz.data)
        return Response(sz.errors)

class RetrieveDeleteStory(generics.RetrieveDestroyAPIView):
    serializer_class = StroySerializer
    queryset = ProfileStory.objects.all()

    def delete(self, request, user_id, story_id, *args, **kwargs):
        user = get_object_or_404(User, id = user_id)
        story = get_object_or_404(ProfileStory, user = user, id = story_id)
        story.delete()
        return Response({"message" : "Deleted succesfully!"})
    
    def get(self, request, user_id, story_id, *args, **kwargs):
        user = get_object_or_404(User, id=user_id)
        story = get_object_or_404(ProfileStory, user=user, id=story_id)
        sz = StroySerializer(story)  # Corrected typo
        return Response(sz.data)
    
class LikePostAPI(APIView):
    def post(self, request, user_id, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id = post_id)
        user = get_object_or_404(User, id = user_id)
        if post.likes.filter(id = user_id).exists():
            post.likes.remove(user)
            return Response({"message" : "Post Unliked"})
        else:
            post.likes.add(user)
            return Response({"message" : "Post liked"})

class ListPostComment(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def post(self, request, post_id, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"message" : 'Please login!'})
        user = request.user
        post = get_object_or_404(Post, id = post_id)
        sz = CommentSerializer(data = request.data)
        if sz.is_valid():
            sz.save(user = user, post = post)
            return Response(sz.data)
        return Response(sz.errors)

class DeleteComment(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def delete(self, request, post_id, comment_id, *args, **kwargs):
        comment = get_object_or_404(Comment, id = comment_id)
        post = get_object_or_404(Post, id = post_id)
        user = request.user
        if user == post.user or comment.user == user:
            comment.delete()
            return Response({"message" : "Comment has been deleted"})
        
        return Response({"message" : "you are not authenticated"})
    
class LikeComment(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, comment_id , *args, **kwargs):
        user = request.user
        comment = get_object_or_404(Comment, id = comment_id)
        if comment.likes.filter(id = user.id):
            comment.likes.remove(user)
            return Response({"message" : "Comment Unliked"})
        comment.likes.add(user)
        return Response({"message" : "Comment Liked"})

        
    
        




