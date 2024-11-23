from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path("<int:post_id>/media/",views.UploadContent.as_view(), name = "upload-content"),
    path('<int:post_id>/', views.PostRetrieveDeleteUpdate.as_view(), name='post-retrieve-delete-update'),
    path('<int:user_id>/posts/', views.PostListCreateAPIView.as_view(), name='post-list-create'),
    path('story/<int:user_id>/', views.CreateListStory.as_view(), name='story-list-create'),
    path('story/<int:user_id>/<int:story_id>', views.RetrieveDeleteStory.as_view(), name='story-get-delete'),
    path('like/<int:user_id>/<int:post_id>', views.LikePostAPI.as_view(), name = "Like-a-post"),
    path('<int:post_id>/comments', views.ListPostComment.as_view(), name = "comment"),
    path('<int:post_id>/comments/<int:comment_id>', views.DeleteComment.as_view(), name = "delete-comment"),
    path('comments/<int:comment_id>/like', views.LikeComment.as_view(), name = "like-comment")
]
