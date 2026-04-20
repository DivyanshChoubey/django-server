from django.urls import path
from service.views import *


urlpatterns = [
    path('Healthcheck', HealthCheckView.as_view(), name='Healthcheck'),
    path('Register', RegisterView.as_view(), name='Register'),
    path('Login', LoginView.as_view(), name='Login'),
    path('Logout', LogoutView.as_view(), name='Logout'),
]
