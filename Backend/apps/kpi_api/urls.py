from django.urls import path

from .views import KpiChatAPIView, KpiUploadAPIView

urlpatterns = [
    path("chat/", KpiChatAPIView.as_view(), name="kpi-chat"),
    path("upload/", KpiUploadAPIView.as_view(), name="kpi-upload"),
]
