from django.db import models
from django.db.models.deletion import SET_NULL
from teams.models import Team
from workouts.models import Workout
from django.contrib.auth.models import User
 

# Create your models here.

class Coach(models.Model):
    # Coach Specific Attributes
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    profile_picture = models.ImageField(upload_to='avatars', default='no_picture.png')
    team = models.ForeignKey(Team, on_delete=models.SET(True))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    formal_title = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)

    secret_key = models.CharField(max_length=20)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    

class Athlete(models.Model):
    # Athlete specific attributes
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    profile_picture = models.ImageField(upload_to='avatars', default='no_picture.png')
    team = models.ForeignKey(Team, on_delete=models.SET(True))

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    # Athlete Specific Attributes
    captain = models.BooleanField(default=False)
    position = models.CharField(max_length=200)

    workouts_rsvped_for = models.ManyToManyField(Workout, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class ScheduleItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True, null=True)
    time_start = models.TimeField(blank=True, null=True)
    time_end = models.TimeField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if (self.name == None):
            return "Name is blank"
        else:
            return self.name
    
    def not_valid(self):

        if (self.name      == None 
        or self.time_start == None 
        or self.time_end   == None 
        or self.day        == None):
            return True
        else:
            return False
        