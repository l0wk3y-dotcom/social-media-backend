from rest_framework import serializers
from .models import *

class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "id"]

class RoomSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many = True, read_only = True)
    class Meta:
        model = Room
        fields = ["participants","updated_at","created_at","new_message_for"]

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["is_read", "room","sender"]