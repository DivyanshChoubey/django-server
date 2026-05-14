from rest_framework import status
from rest_framework.views import APIView

from service.constants import ResponseMessages
from service.models import Teams
from service.utils import ResponseHandler


class TeamDeleteView(APIView):
    def delete(self, request, id):
        try:
            team = Teams.objects.get(id = id)
        except Teams.DoesNotExist:
            return ResponseHandler(
                success=False,
                message=ResponseMessages.TEAM_NOT_FOUND,
                status = status.HTTP_400_BAD_REQUEST
            )

        team.delete()

        return ResponseHandler(
            success=True,
            message=ResponseMessages.TEAM_DELETE_SUCCESS,
            status = status.HTTP_200_OK
        )
