from django.shortcuts import render

# Create your views here.

def create_coach_view(request):
    test_data = None

    context = {
        'test_data':test_data,
    }

    return render(request, 'accounts/create_coach.html', context)