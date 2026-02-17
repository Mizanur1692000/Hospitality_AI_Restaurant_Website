from django.urls import path

from .views import BeverageChatAPIView, BeverageUploadAPIView

urlpatterns = [
    path("chat/", BeverageChatAPIView.as_view(), name="beverage-chat"),
    path("upload/", BeverageUploadAPIView.as_view(), name="beverage-upload"),
]
