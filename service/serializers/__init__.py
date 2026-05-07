__all__=[
    "RegisterSerializer",
    "LoginSerializer",
    "LogoutSerializer",
    "DepartmentSerializer",
    "DepartmentCreateSerializer",
    "DepartmentUpdateSerializer",
    "TeamSerializer",
    "TeamCreateSerializer",
    "TeamUpdateSerializer",
    "TeamsUserMappingSerializers",
    "TaskPRLinkSerializer",
    "DailyTaskSerializer",
    "DailyReportCreateSerializer"
]

from service.serializers.auth_serializer import RegisterSerializer, LoginSerializer, LogoutSerializer
from service.serializers.department_serializer import DepartmentSerializer, DepartmentCreateSerializer, DepartmentUpdateSerializer
from service.serializers.team_serializer import TeamSerializer, TeamCreateSerializer, TeamUpdateSerializer
from service.serializers.teams_user_mapping_serializer import TeamsUserMappingSerializers
from service.serializers.daily_report_serializer import TaskPRLinkSerializer, DailyTaskSerializer, DailyReportCreateSerializer
