from django.db import models
import accounts.models
from django.contrib.auth.models import User



# Create your models here.

class Workout(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(default="Workout description")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    location = models.CharField(max_length=120)

    # Methods
    def __str__(self):
        return self.name


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