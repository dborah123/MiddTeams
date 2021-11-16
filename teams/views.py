from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User

from accounts.models import Athlete, Coach, ScheduleItem
from teams.forms import ScheduleToolForm0, ScheduleToolForm1, ScheduleToolForm2
from teams.utils import count_availible

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


def schedule_tool(request):
    '''
    Scheduling tool
    '''
    user = request.user
    time_form0 = ScheduleToolForm0(request.POST or None)
    time_form1 = ScheduleToolForm1(request.POST or None)
    time_form2 = ScheduleToolForm2(request.POST or None)
    data = [{
                'count': 0,
                'active': False,
                'percent_of_team': None,
            } for _ in range(3)]

    if (Coach.objects.filter(user=user)):
        user_type = Coach.objects.get(user=user)
    else:
        user_type = Athlete.objects.get(user=user)

    if (request.method == "POST"):
        team_qset = Athlete.objects.filter(team=user_type.team)
        num_team = team_qset.count()

        # First Query
        if (time_form0.is_valid() and request.POST.get('day0') != "-1"):
            data[0]['active'] = True
            for athlete in team_qset:
                for item in ScheduleItem.objects.filter(user=athlete.user):
                    if (count_availible(request.POST.get('time_start0'), 
                                        request.POST.get('time_end0'), 
                                        request.POST.get('day0'), 
                                        item.time_start, 
                                        item.time_end, 
                                        item.day)):
                        data[0]['count'] += 1

            raw_percent = (data[0]['count'] / num_team) * 100
            data[0]['percent_of_team'] = f"{raw_percent:.1f}"
        else:
            data[0]['active'] = False


        # Second Query
        if (time_form1.is_valid() and request.POST.get('day1') != "-1"):
            data[1]['active'] = True
            for athlete in team_qset:
                for item in ScheduleItem.objects.filter(user=athlete.user):
                    if (count_availible(request.POST.get('time_start0'), 
                                        request.POST.get('time_end1'), 
                                        request.POST.get('day1'), 
                                        item.time_start, 
                                        item.time_end, 
                                        item.day)):
                        data[1]['count'] += 1

            raw_percent = (data[1]['count'] / num_team) * 100
            data[1]['percent_of_team'] = f"{raw_percent:.1f}"
        else:
            data[1]['active'] = False

        

        # Third Query
        if (time_form2.is_valid() and request.POST.get('day2') != "-1"):
            data[2]['active'] = True
            for athlete in team_qset:
                for item in ScheduleItem.objects.filter(user=athlete.user):
                    if (count_availible(request.POST.get('time_start2'), 
                                        request.POST.get('time_end2'), 
                                        request.POST.get('day2'), 
                                        item.time_start, 
                                        item.time_end, 
                                        item.day)):
                        data[2]['count'] += 1

            raw_percent = (data[2]['count'] / num_team) * 100
            data[2]['percent_of_team'] = f"{raw_percent:.1f}"
        else:
            data[2]['active'] = False
    else:
        for item in data:
            item['active'] = False

    print(data)

    context = {
        'time_form0': time_form0,
        'time_form1': time_form1,
        'time_form2': time_form2,

        'data': data,
    }

    return render(request, 'teams/schedule-tool.html', context)

