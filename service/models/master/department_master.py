from django.db import models


class DepartmentMaster(models.Model):
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(
        "service.Users",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='department_master'
