from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

route = DefaultRouter()
route.register("user",views.UserProfileAPI,basename="User-profile")
route.register("admin",views.AdminProfileAPI,basename="Admin-profile")
route.register("mob",views.MobProfileAPI,basename="Mob-profile")

urlpatterns = [
    path("",include(route.urls)),
    path("user/<int:pk>/picture",views.ImageUploadView.as_view(),name="add-picture"),
    path("user/<int:pk>/follow",views.FollowUser.as_view(),name="follow-user"),

]
