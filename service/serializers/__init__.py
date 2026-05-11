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
    "DailyReportCreateSerializer",
    "DailyReportGetSerializer",
    "DailyReportUpdateSerializer",
    "DailyResportUpdateview"
]

from service.serializers.authentication.auth_serializer import RegisterSerializer, LoginSerializer, LogoutSerializer
from service.serializers.master.department_serializer import DepartmentSerializer, DepartmentCreateSerializer, DepartmentUpdateSerializer
from service.serializers.team.team_serializer import TeamSerializer, TeamCreateSerializer, TeamUpdateSerializer
from service.serializers.team.teams_user_mapping_serializer import TeamsUserMappingSerializers
from service.serializers.reports.daily_report_serializer import TaskPRLinkSerializer, DailyTaskSerializer, DailyReportCreateSerializer
from service.serializers.reports.daily_report_get_serializer import DailyReportGetSerializer
from service.serializers.reports.daily_report_update_serializer import DailyReportUpdateSerializer
