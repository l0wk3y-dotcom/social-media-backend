from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import *
from .serializers import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet


class UserProfileAPI(ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

class ImageUploadView(APIView):
    #user roles should be able to edit this: mob or user itself: we need to add authentication for that
    def post(self, request, pk, *args, **kwargs):
        serializer = ImageUploadSerializer(data=request.data)
        user = get_object_or_404(User, pk=pk)

        if serializer.is_valid():
            # Get the uploaded file from the request
            image = serializer.validated_data['image']
            # Save the file to the default storage location
            file_path = default_storage.save(f'PP/{image.name}', ContentFile(image.read()))
            # Create the full URL to access the file
            image_url = request.build_absolute_uri(file_path)

            # Create a ProfilePicture object
            pic_obj = ProfilePicture.objects.create(profile_picture=file_path)

            # Link ProfilePicture to UserProfile
            user_profile = getattr(user, 'userprofile', None)
            if user_profile is not None:
                user_profile.profile_picture = pic_obj
                user_profile.save()
                return Response({"image_path": f"https://127.0.0.1{file_path}" }, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "User does not have a profile."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk = pk)
        user_profile = user.userprofile 
        profile_picture = user_profile.profile_picture 
        if profile_picture:
            image_url = profile_picture.profile_picture.url  # This is the URL of the profile picture
        else:
            image_url = None 
        return Response({f"username : {user.username}, image_url : {image_url}"})
    


#this is the *adminmodel* stuff---------------------------------------
class AdminProfileAPI(ModelViewSet):
    serializer_class = AdminProfileSerializer
    queryset = AdminProfile.objects.all()

#this is the *adminmodel* stuff---------------------------------------
class MobProfileAPI(ModelViewSet):
    serializer_class = MobProfileSerializer
    queryset = MobProfile.objects.all()


class FollowUser(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        # Get the current user's profile
        try:
            user_profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            return Response({"message": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

        # Use the follow method on the user's profile to follow the target user by pk
        follow_obj, created = user_profile.follow(pk)
        
        if not follow_obj:
            return Response({"message": "Unable to follow user"}, status=status.HTTP_304_NOT_MODIFIED)
        else:
            return Response({
                "follower": f"{request.user.username}",
                "followed": follow_obj.followed.username
            }, status=status.HTTP_200_OK)
        



