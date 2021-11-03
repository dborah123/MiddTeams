from django.shortcuts import render
from django.db.models.query_utils import Q
from .forms import WorkoutForm
from accounts.models import Coach, Athlete
from .models import Workout
from datetime import date, timedelta
import json

# Create your views here.

def home_view1(request):
    workout_form = WorkoutForm(request.POST or None)
    '''
    Home page view
    '''
    # Initialize data
    test_data = "hello world"


    user=request.user

    print(workout_form.is_valid())

    if(request.method == "POST" 
        and workout_form.is_valid() 
        and request.POST.get("submit")):

        if(Coach.objects.filter(user=user).exists()):
            coach = Coach.objects.get(user=user)
            team = coach.team
        else:
            athlete = Athlete.objects.get(user=user)
            team = athlete.team

        workout = workout_form.save(commit=False)
        workout.creator=user

        if (
            Workout.objects.filter(
                Q(time_start__range=[workout.time_start, workout.time_end], date=workout.date, team=team) |
                Q(time_end__range=[workout.time_start, workout.time_end], date=workout.date, team=team) |
                Q(time_start__lte=workout.time_start, time_end__gte=workout.time_end, date=workout.date, team=team)
            )):
            already_exists = 1
        else:
            already_exists = 2
            workout.save()

        workout = WorkoutForm()

def home_view(request):
    # Query if the user is a coach
    is_coach_user = Coach.objects.filter(user=request.user)

    # Redirect user depending on type of user
    if(is_coach_user):
        return coach_workouts_view(request)
    else:
        return athlete_workouts_view(request)

# to be worked on later 
def coach_workouts_view(request):
    
    user=request.user

    workout_form = WorkoutForm(request.POST or None)

    user_coach = Coach.objects.get(user=user)
    team = user_coach.team

    workouts = []

    for workout in Workout.objects.filter(team=team, date__range=[date.today(), date.today() + timedelta(days=14)]):
        d = {
            "name":workout.name,
            "workout_description":workout.description,
            "creator_first":workout.creator.first_name,
            "creator_last":workout.creator.last_name,
            "workout_date":workout.date,
            "time_start":workout.time_start,
            "time_end":workout.time_end,
            "location":workout.location,
            'rsvp': True,
            "pk":workout.pk
        }
        workouts.append(d)

    if(request.method == "POST" 
        and workout_form.is_valid() 
        and request.POST.get("submit")):

        workout = workout_form.save(commit=False)
        workout.creator = user
        workout.team = team

        if (workout.not_valid() or 
            Workout.objects.filter(
                Q(time_start__range=[workout.time_start, workout.time_end], date=workout.date, team=team) |
                Q(time_end__range=[workout.time_start, workout.time_end], date=workout.date, team=team) |
                Q(time_start__lte=workout.time_start, time_end__gte=workout.time_end, date=workout.date, team=team)
            )):
            print("here")
            already_exists = 1
        else:
            already_exists = 2
            workout.save()

        workout_form = WorkoutForm()
        
    # Create context
    context = {
        'workout_form':workout_form,
        'workouts': workouts,
    }

    return render(request, 'workouts/home.html', context)


    # view for athletes
def athlete_workouts_view(request):

    user=request.user

    user_athlete = Athlete.objects.get(user=user)
    team = user_athlete.team

    workout_form = WorkoutForm(request.POST or None)

    workouts = []

    for workout in Workout.objects.filter(team=team, date__range=[date.today(),date.today() + timedelta(days=14)]):
        d = {
            "name":workout.name,
            "workout_description":workout.description,
            "creator_first":workout.creator.first_name,
            "creator_last":workout.creator.last_name,
            "workout_date":workout.date,
            "time_start":workout.time_start,
            "time_end":workout.time_end,
            "location":workout.location,
            "pk":workout.pk
        }
        workouts.append(d)

    if(request.method == "POST" 
        and workout_form.is_valid() 
        and request.POST.get("submit")):

        workout = workout_form.save(commit=False)
        workout.creator = user
        workout.team = team


        if (workout.not_valid() or
            Workout.objects.filter(
                Q(time_start__range=[workout.time_start, workout.time_end], date=workout.date, team=team) |
                Q(time_end__range=[workout.time_start, workout.time_end], date=workout.date, team=team) |
                Q(time_start__lte=workout.time_start, time_end__gte=workout.time_end, date=workout.date, team=team)
            )):
            already_exists = 1
        else:
            already_exists = 2
            workout.save()

        workout = WorkoutForm()
        
    # Create context
    context = {
        'workout_form':workout_form,
        'workouts': workouts,

    }

    return render(request, 'workouts/home.html', context)