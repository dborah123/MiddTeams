from django.db import models

# Create your models here.

class Team(models.Model):
    name = models.CharField(max_length=120)
    team_code = models.CharField(max_length=20)

    def __str__(self):
        return self.name