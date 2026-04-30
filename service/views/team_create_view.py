from rest_framework.views import APIView
from service.serializers import TeamCreateSerializer
from rest_framework.response import Response
from service.constants import ResponseMessages
from rest_framework import status
from service.models import Teams, Users


class TeamCreateView(APIView):
    def post(self, request):
        serializer = TeamCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    "success": False,
                    "message": ResponseMessages.INVALID_DATA,
                    "errors": serializer.errors
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        name = serializer.validated_data.get("name")
        description = serializer.validated_data.get("description")
        created_by = serializer.validated_data.get("created_by")

        user = None
        if created_by is not None:
            try:
                user = Users.objects.get(id = created_by)
            except Users.DoesNotExist:
                return Response(
                    {
                        "success": False,
                        "message": ResponseMessages.INVALID_CREATED_BY
                    },
                    status = status.HTTP_400_BAD_REQUEST 
                )

        team = Teams.objects.create(
            name = name,
            description = description,
            created_by = user
        )

        return Response(
            {
                "success": True,
                "message": ResponseMessages.TEAM_CREATED,
                "data": {
                    "id": team.id,
                    "name":team.name
                }
            },
            status = status.HTTP_201_CREATED
        )
