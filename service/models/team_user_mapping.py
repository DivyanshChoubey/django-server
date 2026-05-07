from django.db import models

from service.models import Teams, Users


class TeamUserMapping(models.Model):
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table='team_user_mapping'
        unique_together = ('team', 'user')
