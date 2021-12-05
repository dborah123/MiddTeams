import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from datetime import date, datetime, timedelta, time

from accounts.models import Athlete, Coach, ScheduleItem
from teams.forms import ScheduleToolForm0, ScheduleToolForm1, ScheduleToolForm2
from teams.utils import is_availible
from workouts.models import ABSENCE_OPTIONS, ExcuseRequest

# Create your views here.
@login_required(login_url='/login/')
def roster_view(request):
    '''
    Displays roster of the team the user is on
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
    
    # Querying for entire roster (athletes+coaches)
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


@login_required(login_url='/login/')
def schedule_tool(request):
    '''
    Scheduling tool v1: User an query up to 3 specific meeting times and see who is availible
                        NOTE: will only query the classes as it is assumed coaches will know
                        when their practices are
    '''
    # Get user
    user = request.user

    # Initialize 3 different query forms
    time_form0 = ScheduleToolForm0(request.POST or None)
    time_form1 = ScheduleToolForm1(request.POST or None)
    time_form2 = ScheduleToolForm2(request.POST or None)

    # Initialize data for each potential query
    data = [{
                'count': 0,
                'active': False,
                'percent_of_team': None,
            } for _ in range(3)]
    
    # Get user type
    if (Coach.objects.filter(user=user)):
        user_type = Coach.objects.get(user=user)
    else:
        user_type = Athlete.objects.get(user=user)

    if (request.method == "POST"):
        # Get team and number of athletes on team
        team_qset = Athlete.objects.filter(team=user_type.team)
        num_team = team_qset.count()

        # First Query
        if (time_form0.is_valid() and request.POST.get('day0') != "-1"):
            data[0]['active'] = True
            for athlete in team_qset:
                for item in ScheduleItem.objects.filter(user=athlete.user):
                    if (is_availible(datetime.strptime(request.POST.get('time_start0'), '%H:%M').time(), 
                                        datetime.strptime(request.POST.get('time_end0'), '%H:%M').time(), 
                                        int(request.POST.get('day0')), 
                                        item.time_start, 
                                        item.time_end, 
                                        item.day)):
                        data[0]['count'] += 1

            # Calculations
            data[0]['count'] = num_team - data[0]['count']
            raw_percent = (data[0]['count'] / num_team) * 100
            data[0]['percent_of_team'] = f"{raw_percent:.1f}"
        else:
            data[0]['active'] = False


        # Second Query
        if (time_form1.is_valid() and request.POST.get('day1') != "-1"):
            data[1]['active'] = True
            for athlete in team_qset:
                for item in ScheduleItem.objects.filter(user=athlete.user):
                    if (is_availible(datetime.strptime(request.POST.get('time_start1'), '%H:%M').time(), 
                                        datetime.strptime(request.POST.get('time_end1'), '%H:%M').time(), 
                                        request.POST.get('day1'), 
                                        item.time_start, 
                                        item.time_end, 
                                        item.day)):
                        data[1]['count'] += 1

            # Calculations
            data[1]['count'] = num_team - data[1]['count']
            raw_percent = (data[1]['count'] / num_team) * 100
            data[1]['percent_of_team'] = f"{raw_percent:.1f}"
        else:
            data[1]['active'] = False

        

        # Third Query
        if (time_form2.is_valid() and request.POST.get('day2') != "-1"):
            data[2]['active'] = True
            for athlete in team_qset:
                for item in ScheduleItem.objects.filter(user=athlete.user):
                    if (is_availible(datetime.strptime(request.POST.get('time_start2'), '%H:%M').time(), 
                                        datetime.strptime(request.POST.get('time_end2'), '%H:%M').time(), 
                                        datetime.strptime(request.POST.get('day2')), 
                                        item.time_start, 
                                        item.time_end, 
                                        item.day)):
                        data[2]['count'] += 1

            # Calculations
            data[2]['count'] = num_team - data[2]['count']
            raw_percent = (data[2]['count'] / num_team) * 100
            data[2]['percent_of_team'] = f"{raw_percent:.1f}"
        else:
            data[2]['active'] = False
    else:
        for item in data:
            item['active'] = False

    context = {
        'time_form0': time_form0,
        'time_form1': time_form1,
        'time_form2': time_form2,

        'data': data,
    }

    return render(request, 'teams/schedule-tool.html', context)


@login_required(login_url='/login/')
def absences_view(request):
    '''
    Handles absences from practice, displaying them only to coaches
    '''
    user = request.user
    if (Coach.objects.filter(user=user)):
        team = Coach.objects.get(user=user).team
    else:
        return redirect('/1')

    # Initialize lists for storing absences in categories
    todays_absences = []
    past_absences = []
    future_absences = []

    # Cycle through different ExcuseRequests
    for item in ExcuseRequest.objects.filter(team=team):
        # Package them into dicts
        d = {
            'workout_name': item.workout.name,
            'workout_date': item.workout.date,
            'first_name': item.account.user.first_name,
            'last_name': item.account.user.last_name,
            'reason': ABSENCE_OPTIONS[int(item.reason)-1][1],
            'explanation': item.explanation,
            'workout_pk': item.workout.pk,
            'pk': item.pk,
        }
        # Categorize them
        if (item.workout.date != None):
            if (item.workout.date < date.today()):
                past_absences.append(d)
            elif (item.workout.date > date.today()):
                future_absences.append(d)
            else:
                todays_absences.append(d)


    context = {
        'past_absence': past_absences,
        'todays_absences': todays_absences,
        'future_absences': future_absences,
    }

    return render(request, "teams/absences.html", context)


@login_required(login_url="/login/")
def schedule_tool_v2_view(request):
    '''
    Schedule tool v2: Queries athletes schedules by the hour, counting number availible, and displays them on a weekly calendar
    '''
    # Get user
    user = request.user

    # Get user type and team data
    if (Coach.objects.filter(user=user)):
        user_type = Coach.objects.get(user=user)
    else:
        user_type = Athlete.objects.get(user=user)

    team_qset = Athlete.objects.filter(team=user_type.team)
    team_count = team_qset.count()

    # List for storing info about availibility each hour of the week
    data = []

    # Iterate thru days
    for day in range(7):
        # start each day at 7am
        hour_of_day = datetime(year=1, month=1, day=1, hour=7, minute=0, second=0)

        # Iterate thru rest of the day
        for _ in range(7,24):
            count = 0
            # Perform Query for this hour
            for athlete in team_qset:
                for item in ScheduleItem.objects.filter(user=athlete.user):
                    if (is_availible(hour_of_day.time(), 
                                     (hour_of_day+timedelta(hours=1)).time(), 
                                     day, 
                                     item.time_start, 
                                     item.time_end, 
                                     item.day)):
                        count += 1

            # Package data from this hour for FullCalendar JS
            count = team_count - count
            raw_percent = (count/team_count) * 100
            title = f"Availible: {count} ({raw_percent:.1f}%)"
            d = {
                'title': title,
                'startTime': hour_of_day.strftime("%H:%M"),
                'endTime': (hour_of_day + timedelta(hours=1)).time().strftime("%H:%M"),
                'daysOfWeek': [day],
                'startReoccur': '2020-9-9',
                'endReoccur': '2020-14-12',
                'color': ''
            }

            # Change color of event depending on how many availible
            if (raw_percent > 85):
                d['color']  = '#3c804f'
            elif (raw_percent > 70):
                d['color']  = '#d4cc2f'
            else:
                d['color'] = '#b32520'
            data.append(d)

            # Update to next hour
            hour_of_day += timedelta(hours=1)


    context = {
        'data':json.dumps(data),
    }

    return render(request, "teams/schedule-v2.html", context)