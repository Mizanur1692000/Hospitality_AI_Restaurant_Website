from django.urls import path
from .views import RecipeChatAPIView, RecipeUploadAPIView

urlpatterns = [
    path("chat/", RecipeChatAPIView.as_view(), name="recipe-chat"),
    path("upload/", RecipeUploadAPIView.as_view(), name="recipe-upload"),
]
