from django.db import models

from service.constants import Constants


class Users(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    bio = models.TextField(max_length=250, blank=True)
    department = models.ForeignKey(
        "service.DepartmentMaster",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    position_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    user_type = models.CharField(max_length=20, choices=Constants.USER_TYPES, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='users'
