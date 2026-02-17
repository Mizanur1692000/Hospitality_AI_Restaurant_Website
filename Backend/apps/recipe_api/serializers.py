from rest_framework import serializers


class RecipeChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=8000, trim_whitespace=False)


class RecipeChatResponseSerializer(serializers.Serializer):
    html_response = serializers.CharField()


class RecipeUploadResponseSerializer(serializers.Serializer):
    html_response = serializers.CharField()
