from django.db import models
import accounts.models
from django.contrib.auth.models import User
from teams.models import Team


class Workout(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=120,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(blank=True,null=True)
    time_start = models.TimeField(blank=True,null=True)
    time_end = models.TimeField(blank=True,null=True)
    location = models.CharField(max_length=120,blank=True,null=True)

    # Methods
    def __str__(self):
        return self.name

    def not_valid(self):
        if (self.name == None
        or self.description == None 
        or self.date == None
        or self.time_start == None 
        or self.time_end == None
        or self.location == None):
            return True
        else:
            return False

EXCUSE_OPTIONS = (
    ('#1', 'Sick'),
    ('#2', 'Injured'),
)

class ExcuseRequest(models.Model):
    account = models.ForeignKey("accounts.Athlete", on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    reason = models.CharField(choices=EXCUSE_OPTIONS, max_length=200)
    explanation = models.TextField(default="Excuse explanation")