from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from Accounts.user_model import User
    
class Room(models.Model):
    participants = models.ManyToManyField(User, related_name="rooms", blank = True)
    updated_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    new_message_for = models.ForeignKey(User, related_name="unread_rooms", on_delete = models.CASCADE)

class Message(models.Model):
    room = models.ForeignKey(Room, related_name="messages", on_delete=models.CASCADE, null = True, blank = True)
    sender = models.ForeignKey(User, related_name = "sent_messages", on_delete=models.CASCADE)
    reciever = models.ForeignKey(User, related_name = "recieved_messages", on_delete=models.CASCADE)
    content = models.TextField(default = ".")
    is_read = models.BooleanField(default = False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ["sender", "reciever"]


@receiver(post_save, sender=Message)
def new_message(sender, instance, created, *args, **kwargs):
    if created:
        rooms = Room.objects.filter(participants__in = [instance.reciever, instance.sender]).distinct()
        if not rooms.exists():
            room = Room.objects.create(updated_at = now(), new_message_for = instance.reciever)
            room.participants.add(instance.sender, instance.reciever)
            room.save()
            instance.room = room
            
        else:
            instance.room = rooms.first()
            instance.room.updated_at = now()
            instance.room.new_message_for = instance.reciever
            instance.room.save()
        instance.save()
