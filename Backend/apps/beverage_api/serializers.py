from __future__ import annotations

from rest_framework import serializers


class BeverageChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(allow_blank=False, trim_whitespace=True, max_length=8000)


class BeverageChatResponseSerializer(serializers.Serializer):
    html_response = serializers.CharField()


class BeverageUploadRequestSerializer(serializers.Serializer):
    required_csv = serializers.FileField(required=True)
    analysis_type = serializers.ChoiceField(
        required=False,
        allow_null=True,
        choices=(
            "liquor_cost_analysis",
            "bar_inventory_analysis",
            "beverage_pricing_analysis",
            "auto",
        ),
    )

    def validate_required_csv(self, file_obj):
        name = getattr(file_obj, "name", "") or ""
        if not name.lower().endswith(".csv"):
            raise serializers.ValidationError("required_csv must be a .csv file")
        return file_obj


class BeverageUploadResponseSerializer(serializers.Serializer):
    html_response = serializers.CharField()
