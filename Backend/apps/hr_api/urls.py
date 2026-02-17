from django.urls import path

from .views import HrChatAPIView, HrUploadAPIView

urlpatterns = [
    path("chat/", HrChatAPIView.as_view(), name="hr-chat"),
    path("upload/", HrUploadAPIView.as_view(), name="hr-upload"),
]
