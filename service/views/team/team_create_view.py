from rest_framework import status
from rest_framework.views import APIView

from service.constants import ResponseMessages
from service.models import Teams, Users
from service.serializers import TeamCreateSerializer
from service.utils import ResponseHandler


class TeamCreateView(APIView):
    def post(self, request):
        serializer = TeamCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return ResponseHandler(
                success=False,
                message=ResponseMessages.INVALID_DATA,
                errors=serializer.errors,
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
                return ResponseHandler(
                    success=False,
                    message=ResponseMessages.INVALID_CREATED_BY,
                    status = status.HTTP_400_BAD_REQUEST 
                )

        team = Teams.objects.create(
            name = name,
            description = description,
            created_by = user
        )

        return ResponseHandler(
            success=True,
            message= ResponseMessages.TEAM_CREATED,
            data={
                "id": team.id,
                "name":team.name
            },
            status = status.HTTP_201_CREATED
        )
