from django.shortcuts import render
from .forms import CoachCreationForm

# Create your views here.

def create_coach_view(request):
    test_data = None
    coach_create_form = CoachCreationForm()

    context = {
        'test_data':test_data,
        'coach_create_form': coach_create_form,
    }

    return render(request, 'accounts/create_coach.html', context)