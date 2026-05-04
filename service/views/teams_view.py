from rest_framework.views import APIView
from service.serializers import TeamSerializer
from service.models import Teams
from rest_framework.response import Response
from service.constants import ResponseMessages
from rest_framework import status



class TeamsView(APIView):
    def get(self, request):
        teams = Teams.objects.all().order_by("-id")
        serializer = TeamSerializer(teams, many=True)

        return Response(
            {
                "success": True,
                "message": ResponseMessages.TEAM_FETCH,
                "data": serializer.data
            },
            status = status.HTTP_200_OK
        )
