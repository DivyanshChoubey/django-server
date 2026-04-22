from django.db import models
from service.models import AdminUser
from service.models import DepartmentMaster


class Teams(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=256, blank=True, null=True)
    created_by = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True) 
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='teams'
