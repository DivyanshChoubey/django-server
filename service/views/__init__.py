__all__ = [
    "HealthCheckView",
    "RootView",
    "RegisterView",
    "LoginView",
    "LogoutView",
    "DepartmentView",
    "TeamsView",
    "TeamCreateView",
    "TeamUpdateView",
    "TeamDeleteView",
    "DailyReportCreateView",
    "DailyReportView",
    "DailyReportUpdateView"
]

from service.views.healthcheck_view import HealthCheckView
from service.views.root_view import RootView
from service.views.authentication.register_view import RegisterView
from service.views.authentication.login_view import LoginView
from service.views.authentication.logout_view import LogoutView
from service.views.master.department_view import DepartmentView
from service.views.team.teams_view import TeamsView
from service.views.team.team_create_view import TeamCreateView
from service.views.team.team_update_view import TeamUpdateView
from service.views.team.team_delete_view import TeamDeleteView
from service.views.reports.daily_report_create_view import DailyReportCreateView
from service.views.reports.daily_report_view import DailyReportView
from service.views.reports.daily_report_update_view import DailyReportUpdateView
