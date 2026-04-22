from django.db import models
from service.models import AdminUser


class DepartmentMaster(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(AdminUser, on_delete=models.SET_NULL, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='department_master'
