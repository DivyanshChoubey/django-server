__all__ = [
    "HealthCheckView",
    "RootView",
    "RegisterView",
    "LoginView",
    "LogoutView",
    "DepartmentsView",
    "DepartmentCreateView",
    "DepartmentUpdateView",
    "TeamsView",
    "TeamCreateView",
    "TeamUpdateView",
    "TeamDeleteView",
    "DailyReportCreateView",
]

from service.views.healthcheck_view import HealthCheckView
from service.views.root_view import RootView
from service.views.register_view import RegisterView
from service.views.login_view import LoginView
from service.views.logout_view import LogoutView
from service.views.departments_view import DepartmentsView
from service.views.department_create_view import DepartmentCreateView
from service.views.department_update_view import DepartmentUpdateView
from service.views.teams_view import TeamsView
from service.views.team_create_view import TeamCreateView
from service.views.team_update_view import TeamUpdateView
from service.views.team_delete_view import TeamDeleteView
from service.views.daily_report_create_view import DailyReportCreateView
