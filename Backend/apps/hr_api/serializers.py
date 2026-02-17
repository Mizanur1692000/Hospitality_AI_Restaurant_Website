from __future__ import annotations

from rest_framework import serializers


class HrChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(allow_blank=False, trim_whitespace=True, max_length=8000)


class HrChatResponseSerializer(serializers.Serializer):
    html_response = serializers.CharField()


class HrUploadRequestSerializer(serializers.Serializer):
    required_csv = serializers.FileField(required=True)
    optional_csv = serializers.FileField(required=False, allow_null=True)

    def validate_required_csv(self, file_obj):
        name = getattr(file_obj, "name", "") or ""
        if not name.lower().endswith(".csv"):
            raise serializers.ValidationError("required_csv must be a .csv file")
        return file_obj

    def validate_optional_csv(self, file_obj):
        if file_obj is None:
            return None
        name = getattr(file_obj, "name", "") or ""
        if name and not name.lower().endswith(".csv"):
            raise serializers.ValidationError("optional_csv must be a .csv file")
        return file_obj


class HrUploadResponseSerializer(serializers.Serializer):
    html_response = serializers.CharField()
