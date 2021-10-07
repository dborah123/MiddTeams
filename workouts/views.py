from django.shortcuts import render

# Create your views here.

def home_view(request):
    '''
    Home page view
    '''
    # Initialize data
    test_data = "hello world"

    # Create context
    context = {
        'test_data':test_data,
    }

    return render(request, 'workouts/home.html', context)