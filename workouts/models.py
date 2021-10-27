from django.db import models
import accounts.models
from django.contrib.auth.models import User
from teams.models import Team



# Create your models here.

class Workout(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=120)
    description = models.TextField(default="Workout description")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    location = models.CharField(max_length=120)

    # Methods
    def __str__(self):
        return self.name

    def not_valid(self):
        if (self.name == None
        or self.description == None 
        or self.creator == None 
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
    # Incomplete...fix later
)

class ExcuseRequest(models.Model):
    account = models.ForeignKey("accounts.Athlete", on_delete=models.CASCADE)
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    reason = models.CharField(choices=EXCUSE_OPTIONS, max_length=200)
    explanation = models.TextField(default="Excuse explanation")