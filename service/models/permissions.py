from django.db import models


class Permissions(models.Model):
    permission_name = models.CharField(max_length=50, unique=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='permissions'
