from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *
from .models import *
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
# Create your views here.


class ListRoomsCreateMessageAPIView(generics.ListCreateAPIView):


    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"message" : "you are not authenticated"})
        rooms = Room.objects.filter(participants = request.user)
        sz = RoomSerializer(rooms, many = True)
        return Response(sz.data)


class ListRoomAPIView(generics.ListAPIView):
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]  # Ensures user is authenticated before accessing

    def get_queryset(self):
        return Room.objects.filter(participants=self.request.user)
    
    
class CreateMessageAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]  # Ensures user is authenticated before accessing
    serializer_class = MessageSerializer
    queryset = Message.objects.all()

    def post(self, request, *args, **kwargs):
        sz = MessageSerializer(data = request.data)
        if sz.is_valid():
            sz.save(sender = request.user)
            return Response(sz.data)
        return Response(sz.errors)

class ListRoomMessagesAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    def get_queryset(self):
        room_id = self.kwargs["pk"]
        room = get_object_or_404(Room, id = room_id)
        messages = Message.objects.filter(room = room)
        return messages
    

    

class RetrieveDestromMessage(generics.RetrieveDestroyAPIView):
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    identifier = "pk"