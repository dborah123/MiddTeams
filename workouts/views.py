from django.shortcuts import render
from django.db.models.query_utils import Q
from .forms import WorkoutForm
from accounts.models import Coach, Athlete
from .models import Workout
from datetime import date, timedelta
import json

# Create your views here.

def home_view(request):
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

    def profile_view(request):
            # Query if the user is a coach
        is_coach_user = Coach.objects.get(user=request.user)

        # Redirect user depending on type of user
        if(is_coach_user):
            return coach_workouts_view(request)
        else:
            return athlete_workouts_view(request)
    
    # to be worked on later 
    def coach_workouts_view(request):
        return

    # view for athletes
    def athlete_workouts_view(request):

        user=request.user

        user_qset = Athlete.objects.get(user=user)

        for workout in Workout.objects.filter(team=user_qset.team,date_start__range=[date.today(),date.today() + timedelta(days=14)]):
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
        workout_form = WorkoutForm(request.POST or None)

        if(request.method == "POST" 
            and workout_form.is_valid() 
            and request.POST.get("submit")):

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
            
    # Create context
    context = {
        'test_data':test_data,
        'workout_form':workout_form,
    }

    return render(request, 'workouts/home.html', context)