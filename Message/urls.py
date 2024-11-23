from django.urls import path
from . import views
urlpatterns = [
    path("", views.ListRoomAPIView.as_view(), name = "list-rooms"),
    path("create", views.CreateMessageAPIView.as_view(), name = "create-message"),
    path("room/<int:pk>", views.ListRoomMessagesAPIView.as_view(), name = "room-messages"),
    path("<int:pk>", views.RetrieveDestromMessage.as_view(), name = "retrieve-destroy-message")
]
