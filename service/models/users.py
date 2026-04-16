from django.db import models
from service.models import Roles

class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.ForeignKey(Roles, on_delete=models.DO_NOTHING)
    bio = models.TextField(max_length=250, blank=True)
    position_name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='users'
