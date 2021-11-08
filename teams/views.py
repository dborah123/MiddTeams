from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User

from accounts.models import Athlete, Coach

# Create your views here.
@login_required(login_url='/login/')
def roster_view(request):
    '''
    Displays roster of user
    '''
    # Initializing variables
    athlete_roster = []
    coaches = []

    # Getting user
    user = request.user

    # Getting user's team
    if (Athlete.objects.filter(user=user).exists()):
        user_type = Athlete.objects.get(user=user)
    
    else:
        user_type = Coach.objects.get(user=user)
    
    # Querying for entire roster
    athlete_roster_qset = Athlete.objects.filter(team=user_type.team)

    coach_qset = Coach.objects.filter(team=user_type.team)

    # Packaging querysets for html
    for item in athlete_roster_qset:
        athlete_roster.append({
            'first_name': item.user.first_name,
            'last_name': item.user.last_name,
            'email': item.user.email,
            'position': item.position,
            'captain': item.captain,
            'pk':item.user.pk,
        })

    for item in coach_qset:
        coaches.append({
            'first_name': item.user.first_name,
            'last_name': item.user.last_name,
            'email': item.user.email,
            'formal_title': item.formal_title,
            'pk': item.user.pk,
        })
    
    context = {
        'team': user_type.team,
        'athlete_roster': athlete_roster,
        'coaches': coaches,
    }

    return render(request, 'teams/roster.html', context)