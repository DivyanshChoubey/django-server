from rest_framework import serializers

from service.models import Teams, Users


class TeamsUserMappingSerializers(serializers.Serializer):
    team_id = serializers.PrimaryKeyRelatedField(queryset=Teams.objects.all())
    user_ids = serializers.ListField(
        child=serializers.PrimaryKeyRelatedField(queryset=Users.objects.all())
    )
