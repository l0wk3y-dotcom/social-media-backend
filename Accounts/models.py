from django.db import models
from EcommerceAPI.models import BaseModel
from .user_model import User

class Follow_manager(models.Manager):
    def follow(self, follower, followed):
        if follower != followed:
            follow, created = self.get_or_create(follower = follower, followed = followed)
        return False
    def unfollow(self, follower, followed):
        if follower != followed:
            self.filter(follower = follower, followed = followed).delete()
        else:
            return False
    def is_following(self, follower, followed):
        return self.filter(followed= followed, follower = follower).exists()
        



# all the userroles and user related stuff is written here
class ProfilePicture(models.Model):
    profile_picture = models.ImageField(upload_to="PP/", null=True, blank=True)

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=60)
    profile_picture = models.OneToOneField(ProfilePicture , on_delete=models.CASCADE, null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    DOB = models.DateField()
    banned = models.BooleanField()
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    def __str__(self) -> str:
        return self.user.username
    
    def ban(self):
        self.banned = True
        self.save

    def unban(self):
        self.banned = False
        self.save

    def get_followers(self):
        return Follow.objects.filter(followed = self.user)
    
    def get_followed(self):
        return Follow.objects.filter(follower = self.user)
    
    def follow(self, pk):
        follow_user = User.objects.get(pk=pk)
        Follow_obj = Follow.objects.get_or_create(follower = self.user, followed = follow_user )
        return Follow_obj

    
    class Meta:
        permissions = [("can_ban","can ban a user")]

class Interests(models.Model):
    User = models.ForeignKey(UserProfile, related_name="interests",on_delete=models.CASCADE)
    interest = models.CharField(max_length=20)

class Follow(BaseModel):
    follower = models.ForeignKey(User,on_delete=models.CASCADE)
    followed = models.ForeignKey(User, on_delete=models.CASCADE,related_name="followers")

    class Meta:
        unique_together = ["follower", "followed"]

#here starts the staff user role stuff
class MobProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    employment_date = models.DateField()
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="staff_pictures/", blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}"
    
class AdminProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.OneToOneField(ProfilePicture, on_delete = models.CASCADE, null = True, blank = True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"
    

