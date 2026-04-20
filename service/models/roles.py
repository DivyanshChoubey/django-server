from django.db import models
from service.models import Permissions

class Roles(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_root = models.BooleanField(default=False)
    permission = models.ForeignKey(Permissions, on_delete=models.SET_NULL, null=True, blank=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='roles'
