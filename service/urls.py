from django.urls import path
from service.views import *


urlpatterns = [
    path('Healthcheck', HealthCheckView.as_view(), name='Healthcheck'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
