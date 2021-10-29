from django.shortcuts import render
from django.db.models.query_utils import Q
from .forms import WorkoutForm
from accounts.models import Coach, Athlete
from .models import Workout

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

        print("got here")

        if(Coach.objects.filter(user=user).exists()):
            print("coach if")
            coach = Coach.objects.get(user=user)
            team = coach.team
        else:
            athlete = Athlete.objects.get(user=user)
            team = athlete.team

        workout = workout_form.save(commit=False)
        workout.creator=user

        print(team)
        print(workout.time_start)
        print(workout.time_end)
        print(workout.date)


        if (
            Workout.objects.filter(
                Q(time_start__range=[workout.time_start, workout.time_end], date=workout.date, team=team) |
                Q(time_end__range=[workout.time_start, workout.time_end], date=workout.date, team=team) |
                Q(time_start__lte=workout.time_start, time_end__gte=workout.time_end, date=workout.date, team=team)
            )):
            print("here")
            already_exists = 1
        else:
            already_exists = 2
            print("saved")
            workout.save()

        workout = WorkoutForm()
    
    # Create context
    context = {
        'test_data':test_data,
        'workout_form':workout_form,
    }

    return render(request, 'workouts/home.html', context)