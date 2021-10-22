from django.shortcuts import render
from .forms import WorkoutCreationForm

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

    return render(request, 'workouts/home.html', context)