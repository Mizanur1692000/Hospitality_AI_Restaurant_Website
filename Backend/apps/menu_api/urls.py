from django.urls import path

from .views import MenuChatAPIView, MenuUploadAPIView

urlpatterns = [
    path("chat/", MenuChatAPIView.as_view(), name="menu-chat"),
    path("upload/", MenuUploadAPIView.as_view(), name="menu-upload"),
]
