from rest_framework import serializers


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    role_id = serializers.IntegerField()
    bio = serializers.CharField(required=False, allow_blank=True, max_length=250)
    position_name = serializers.CharField(max_length=50)
