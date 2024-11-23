from django.db import models
from django.core.exceptions import ValidationError
from EcommerceAPI.models import *
from Accounts.user_model import User
from django.utils.timezone import timedelta, now

# Create your models here.
class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    caption = models.CharField(max_length = 100)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank = True)

    def __str__(self) -> str:
        return f"{self.caption} {self.id}"
    
class Content(models.Model):
    MEDIA_TYPE_CHOICES = (
        ("image", "Image"),
        ("video", "Video"),
    )

    def upload_to_path(instance, filename):
        return f"{instance.post.user.username}/{instance.type}s/{filename}"
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="content")
    type = models.CharField(choices=MEDIA_TYPE_CHOICES, max_length=5)
    video = models.FileField(upload_to = upload_to_path, null=True, blank = True)
    image = models.ImageField(upload_to = upload_to_path, null=True, blank = True)

    def get_media(self):
        if self.type == "image":
            return self.image
        
        elif self.type == "video":
            return self.video
        return None
    
    def clean(self):
        if self.type == "image" and not self.image:
            raise ValidationError("you must upload an image when type is set to image! ")
        if self.type == "video" and not self.video:
            raise ValidationError("you must upload an video when type is set to video! ")
        if self.video and self.image:
            raise ValidationError("You can upload only one field in a model either video or image at a time! ")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    

class StoryQueryset(models.QuerySet):
    def delete_expired(self, *args, **kwargs):
        expiration_time = now() - timedelta(minutes=5)
        self.filter(created_at__lt = expiration_time ).delete()

    def all(self, *args, **kwargs):
        self.delete_expired()
        return super().all(*args, **kwargs)

class StoryManager(models.Manager):
    def get_queryset(self):
        return StoryQueryset(self.model, using=self._db)

class ProfileStory(models.Model):
    MEDIA_TYPE_CHOICES = (
        ("image", "Image"),
        ("video", "Video"),
    )

    def upload_to_path(instance, filename):
        return f"{instance.user.username}/{instance.type}s/{filename}"
    user = models.ForeignKey(User, related_name = "stories", on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(choices=MEDIA_TYPE_CHOICES, max_length=5)
    video = models.FileField(upload_to = upload_to_path, null=True, blank = True)
    image = models.ImageField(upload_to = upload_to_path, null=True, blank = True)
    created_at = models.DateTimeField(auto_now=True)


    def get_media(self):
        if self.type == "image":
            return self.image
        
        elif self.type == "video":
            return self.video
        return None
    
    def clean(self):
        if self.type == "image" and not self.image:
            raise ValidationError("you must upload an image when type is set to image! ")
        if self.type == "video" and not self.video:
            raise ValidationError("you must upload an video when type is set to video! ")
        if self.video and self.image:
            raise ValidationError("You can upload only one field in a model either video or image at a time! ")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    objects = StoryManager()

class Comment(BaseModel):
    user = models.ForeignKey(User, related_name = "comments", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField(max_length=300)
    likes = models.ManyToManyField(User, related_name="liked_comments", blank = True)

    def likes_count(self, *args, **kwargs):
        return self.likes.count()
    
    def __str__(self) -> str:
        return f"{self.content} {self.id}"

