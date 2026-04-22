from django.db import models
from service.models import AdminUser


class AdminUserActiveToken(models.Model):
    admin = models.ForeignKey(AdminUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=512, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()

    class Meta:
        db_table='admin_user_active_token'
