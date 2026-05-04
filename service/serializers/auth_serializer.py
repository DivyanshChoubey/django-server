from rest_framework import serializers
from service.constants import Constants


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    bio = serializers.CharField(required=False, allow_blank=True, max_length=250)
    department = serializers.IntegerField(required=False, allow_null=True)
    position_name = serializers.CharField(max_length=50)
    user_type = serializers.ChoiceField(choices=Constants.USER_TYPES)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class LogoutSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
