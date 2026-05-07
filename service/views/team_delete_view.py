from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from service.constants import ResponseMessages
from service.models import Teams


class TeamDeleteView(APIView):
    def delete(self, request, id):
        try:
            team = Teams.objects.get(id = id)
        except Teams.DoesNotExist:
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.TEAM_NOT_FOUND
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        team.delete()

        return Response(
            {
                "success": True,
                "message": ResponseMessages.TEAM_DELETE_SUCCESS
            },
            status = status.HTTP_200_OK
        )
