from rest_framework import serializers
from service.models import Teams


class TeamCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=256)
    created_by = serializers.IntegerField(required=False, allow_null=True)


class TeamUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=50, required=False)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True, max_length=256)


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teams
        fields = [
            "id",
            "name",
            "description",
            "created_by",
            "is_active",
            "created_at",
            "updated_at",
        ]
