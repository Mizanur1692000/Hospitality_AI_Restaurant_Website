from rest_framework import serializers


class StrategicChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(min_length=1, max_length=4000)
