from rest_framework import serializers


class LogoutSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
