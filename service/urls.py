from django.urls import path

from service.views import *

urlpatterns = [
    path('Healthcheck', HealthCheckView.as_view(), name='Healthcheck'),
    path('Register', RegisterView.as_view(), name='Register'),
    path('Login', LoginView.as_view(), name='Login'),
    path('Logout', LogoutView.as_view(), name='Logout'),
    path('Admin/GetDepartments', DepartmentsView.as_view(), name='GetDepartments'),
    path('Admin/CreateDepartment', DepartmentCreateView.as_view(), name='CreateDepartment'),
    path('Admin/UpdateDepartment', DepartmentUpdateView.as_view(), name='UpdateDepartment'),
    path('Admin/GetTeams', TeamsView.as_view(), name='GetTeams'),
    path('Admin/CreateTeam', TeamCreateView.as_view(), name='CreateTeam'),
    path('Admin/UpdateTeam', TeamUpdateView.as_view(), name='UpdateTeam'),
    path('Admin/DeleteTeam/<int:id>',TeamDeleteView.as_view(), name ='DeleteTeam'),
    path('User/CreateDailyReport/Create', DailyReportCreateView.as_view(), name="daily-report-create"),
    path('User/GetDailyReports', DailyReportView.as_view(), name='GetDailyReports'),
    path('User/UpdateDailyReport', DailyResportUpdateview.as_view(),name="UpdateDailyReport" )
]
