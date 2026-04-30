from rest_framework import serializers
from service.models import DepartmentMaster


class DepartmentCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    created_by = serializers.IntegerField(required=False, allow_null=True)


class DepartmentUpdateSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=50)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentMaster
        fields = [
            "id",
            "name",
            "created_by",
            "created_at",
            "updated_at",
        ]