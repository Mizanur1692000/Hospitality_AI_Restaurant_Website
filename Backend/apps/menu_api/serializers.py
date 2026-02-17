from __future__ import annotations

from rest_framework import serializers


class MenuChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(allow_blank=False, trim_whitespace=True, max_length=8000)


class MenuChatResponseSerializer(serializers.Serializer):
    html_response = serializers.CharField()


class MenuUploadResponseSerializer(serializers.Serializer):
    html_response = serializers.CharField()
