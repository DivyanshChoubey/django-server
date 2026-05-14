from rest_framework import status
from rest_framework.views import APIView

from service.constants import ResponseMessages
from service.models import Teams
from service.serializers import TeamSerializer
from service.utils import ResponseHandler


class TeamsView(APIView):
    def get(self, request):
        teams = Teams.objects.all().order_by("-id")
        serializer = TeamSerializer(teams, many=True)

        return ResponseHandler(
            success=True,
            message=ResponseMessages.TEAM_FETCH,
            data=serializer.data,
            status = status.HTTP_200_OK
        )
