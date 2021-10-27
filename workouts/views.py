from django.shortcuts import render
from .forms import WorkoutCreationForm
from accounts.models import Coach, Athlete
from .models import Workout

# Create your views here.

def home_view(request):
    workout_create_form = WorkoutCreationForm()
    '''
    Home page view
    '''
    # Initialize data
    test_data = "hello world"

    # Create context
    context = {
        'test_data':test_data,
        'workout_creation_form':workout_create_form,
    }

    user=request.user

    print(workout_create_form.is_valid())

    if(request.method == "POST" 
        and workout_create_form.is_valid() 
        and request.POST.get("submit")):

        print("got here")

        if(Coach.objects.get(user=user).exists()):
            print("coach if")
            team = Coach.objects.get(user=user)
        else:
            team = Athlete.objects.get(user=user)

        workout = workout_create_form.save(commit=False)
        workout.creator=user

        if (workout.not_valid() or 
            Workout.objects.filter(
                Q(time_start__range=[workout.time_start, workout.time_end], day=workout.day, team=team) |
                Q(time_end__range=[workout.time_start, workout.time_end], day=workout.day, team=team) |
                Q(time_start__lte=workout.time_start, time_end__gte=workout.time_end, day=workout.day, team=team)
            )):
            print("here")
            already_exists = 1
        else:
            already_exists = 2
            print("saved")
            workout.save()

        workout = WorkoutCreationForm()

    return render(request, 'workouts/home.html', context)