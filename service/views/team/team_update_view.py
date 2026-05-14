from rest_framework import status
from rest_framework.views import APIView

from service.constants import ResponseMessages
from service.models import Teams
from service.serializers import TeamUpdateSerializer
from service.utils import ResponseHandler


class TeamUpdateView(APIView):
    def patch(self,request):
        serializer = TeamUpdateSerializer(data=request.data)

        if not serializer.is_valid():
            return ResponseHandler(
                success=False,
                message=ResponseMessages.INVALID_DATA,
                errors=serializer.errors,
                status = status.HTTP_400_BAD_REQUEST
            )

        team_id = serializer.validated_data.get("id")
        name = serializer.validated_data.get("name")
        description = serializer.validated_data.get("description")

        try:
            team = Teams.objects.get(id = team_id)
        except Teams.DoesNotExist:
            return ResponseHandler(
                success=False,
                message=ResponseMessages.TEAM_NOT_FOUND,
                status = status.HTTP_400_BAD_REQUEST
            )

        team.name = name
        team.description = description
        team.save()

        return ResponseHandler(
            success=True,
            message=ResponseMessages.TEAM_UPDATED,
            status = status.HTTP_200_OK
        )
