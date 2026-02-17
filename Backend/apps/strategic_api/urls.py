from django.urls import path
from .views import StrategicChatAPIView, StrategicUploadAPIView

urlpatterns = [
    path("chat/", StrategicChatAPIView.as_view(), name="strategic-chat"),
    path("upload/", StrategicUploadAPIView.as_view(), name="strategic-upload"),
]
