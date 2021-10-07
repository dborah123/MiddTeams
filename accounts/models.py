from django.db import models
from django.db.models.deletion import SET_NULL
from teams.models import Team
from workouts.models import Workout
from django.contrib.auth.models import User
 

# Create your models here.

class Coach(models.Model):
    # Coach Specific Attributes
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='avatars', default='no_picture.png')
    email = models.EmailField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.SET(True))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    formal_title = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)

    secret_key = models.CharField(max_length=20)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class Athlete(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='avatars', default='no_picture.png')
    email = models.EmailField(max_length=200)
    team = models.ForeignKey(Team, on_delete=models.SET(True))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Athlete Specific Attributes
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    captain = models.BooleanField(default=False)
    position = models.CharField(max_length=200)

    workouts_rsvped_for = models.ManyToManyField(Workout)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class ScheduleItem(models.Model):
    user = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    time_start = models.TimeField()
    time_end = models.TimeField()
    day = models.IntegerField()

    def __str__(self):
        return self.name
