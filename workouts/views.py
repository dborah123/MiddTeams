from django.shortcuts import redirect, render
from django.db.models.query_utils import Q
from .forms import WorkoutCreationForm, WorkoutForm
from accounts.models import Coach, Athlete
from .models import Workout
from datetime import date, timedelta
from django.contrib.auth.models import User


from django.contrib.auth.decorators import login_required

# Create your views here.

def home_view1(request):
    workout_form = WorkoutCreationForm(request.POST or None)
    '''
    Home page view
    '''
    # Initialize data
    user=request.user

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

        workout = WorkoutCreationForm()


@login_required(login_url='/login/')
def home_view(request):
    # Query if the user is a coach
    is_coach_user = Coach.objects.filter(user=request.user)

    # Redirect user depending on type of user
    if(is_coach_user):
        return coach_workouts_view(request)
    else:
        return athlete_workouts_view(request)


# to be worked on later
@login_required(login_url='/login/')
def coach_workouts_view(request):
    
    user=request.user

    workout_form = WorkoutCreationForm(request.POST or None)

    user_coach = Coach.objects.get(user=user)
    team = user_coach.team

    workouts = []
    if(request.method == "POST" 
        and workout_form.is_valid() 
        and request.POST.get("submit")):

        workout = workout_form.save(commit=False)
        workout.creator = user
        workout.team = team

        if (workout.not_valid() or 
            Workout.objects.filter(
                Q(time_start__range=[workout.time_start, workout.time_end], date=workout.date, team=team) |
                Q(time_end__range=[workout.time_start, workout.time_end], date=workout.date, team=team) |
                Q(time_start__lte=workout.time_start, time_end__gte=workout.time_end, date=workout.date, team=team)
            )):
            already_exists = 1
        else:
            already_exists = 2
            workout.save()

        workout_form = WorkoutCreationForm()


    for workout in Workout.objects.filter(team=team, date__range=[date.today(), date.today() + timedelta(days=14)]):
        d = {
            "name":workout.name,
            "workout_description":workout.description,
            "creator_first":workout.creator.first_name,
            "creator_last":workout.creator.last_name,
            "workout_date":str(workout.date),
            "time_start":str(workout.time_start),
            "time_end":str(workout.time_end),
            "location":workout.location,
            'rsvp': True,
            "pk":workout.pk
        }
        workouts.append(d)
        
    # Create context
    context = {
        'workout_form':workout_form,
        'workouts': workouts,
    }

    return render(request, 'workouts/home.html', context)


# view for athletes
@login_required(login_url='/login/')
def athlete_workouts_view(request):

    user=request.user
    user_athlete = Athlete.objects.get(user=user)
    team = user_athlete.team

    workout_form = WorkoutCreationForm(request.POST or None)

    workouts = []

    rsvp_conflict = {
        'bool': 0,
        'name': None,
        'time_start': None,
    }

    # Creating a new workout
    if (request.method == "POST" 
        and workout_form.is_valid() 
        and request.POST.get("submit")):

        workout = workout_form.save(commit=False)
        workout.creator = user
        workout.team = team


        workout.save()

        workout_form = WorkoutCreationForm()
    
    # Handling RSVPing
    if (request.method == "POST" ):
        # RSVP user to specified workout
        if (request.POST.get('rsvp-btn', None)):
            workout_rsvp_pk = request.POST.get('rsvp-input')
            workout_to_rsvp = Workout.objects.get(pk=workout_rsvp_pk)

            # Checking if user has already rsvped for a workout
            workout_rsvp_qset = user_athlete.workouts_rsvped_for.filter(
                                Q(date=workout_to_rsvp.date, time_start__range=[workout_to_rsvp.time_start, workout_to_rsvp.time_end]) |
                                Q(date=workout_to_rsvp.date, time_end__range=[workout_to_rsvp.time_start, workout_to_rsvp.time_end]) |
                                Q(date=workout_to_rsvp.date, time_start__lte=workout_to_rsvp.time_start, time_end__gte=workout_to_rsvp.time_end)
                                )

            if (workout_rsvp_qset):
                rsvp_conflict['bool'] = 1
                rsvp_conflict['name'] = str(workout_rsvp_qset[0].name)
                rsvp_conflict['time_start'] =str( workout_rsvp_qset[0].time_start)
            else:
                user_athlete.workouts_rsvped_for.add(workout_to_rsvp)

        # Cancel RSVP to workout
        if (request.POST.get('cancel-btn', None)):
                workout_rsvp_pk = request.POST.get('rsvp-input')
                workout_to_cancel = Workout.objects.get(pk=workout_rsvp_pk)
                user_athlete.workouts_rsvped_for.remove(workout_to_cancel)


    for workout in Workout.objects.filter(
                                            team=team, 
                                            date__range=[date.today(),date.today() + timedelta(days=14)]
                                        ).order_by("date"):
        d = {
            "name":workout.name,
            "workout_description":workout.description,
            "creator_first":workout.creator.first_name,
            "creator_last":workout.creator.last_name,
            "workout_date":str(workout.date),
            "time_start":str(workout.time_start),
            "time_end":str(workout.time_end),
            "location":workout.location,
            "pk":workout.pk,
        }
        
        # Checking if athlete has already rsvpd
        if (user_athlete.workouts_rsvped_for.filter(id=d['pk'])):
            d['rsvp'] = True
        else:
            d['rsvp'] = False

        workouts.append(d)

    # Create context
    context = {
        'workout_form':workout_form,
        'workouts': workouts,
        'rsvp_conflict': rsvp_conflict,
    }

    return render(request, 'workouts/home.html', context)


@login_required
def workout_detail_view(request, **kwargs):
    '''
    Details of workout
    '''
    workout_pk = kwargs.get('pk')
    workout = Workout.objects.get(pk=workout_pk)
    changed = 0
    rsvp_conflict = {
        'bool': 0,
        'name': None,
        'time_start': None,
    }

    # Check if user is coach or athlete
    if (Coach.objects.filter(user=request.user)):
        coach_bool = True
        already_rsvped = True
    else:
        coach_bool = False

    # Handles updating form
    if (request.user == workout.creator 
        or coach_bool):
        workout_form = WorkoutForm(request.POST or None, 
                                    instance=workout)
        not_creator = False
        
        if (workout_form.is_valid()):
            workout_form.save()

            if (workout_form.has_changed()):
                changed = 1

    else:
        workout_form = WorkoutForm(request.POST or None, 
                                    instance=workout,
                                    disable_fields=True)
        not_creator = True

    # Handles deletion of workout
    if (request.POST.get("delete", None)):
        workout.delete()
        return redirect(home_view)

    # Handle RSVPing
    if (request.method == "POST" 
        and not coach_bool):
        # RSVP user to specified workout
        if (request.POST.get('rsvp-btn', None)):
            user_athlete = Athlete.objects.get(user=request.user)

            # Checking if user has already rsvped for a workout
            workout_rsvp_qset = user_athlete.workouts_rsvped_for.filter(
                                Q(date=workout.date, time_start__range=[workout.time_start, workout.time_end]) |
                                Q(date=workout.date, time_end__range=[workout.time_start, workout.time_end]) |
                                Q(date=workout.date, time_start__lte=workout.time_start, time_end__gte=workout.time_end)
                                )

            
            if (workout_rsvp_qset and not workout_rsvp_qset[0] == workout):
                    rsvp_conflict['bool'] = 1
                    rsvp_conflict['name'] = str(workout_rsvp_qset[0].name)
                    rsvp_conflict['time_start'] =str( workout_rsvp_qset[0].time_start)
            else:
                user_athlete.workouts_rsvped_for.add(workout)

        # Cancel RSVP to workout
        if (request.POST.get('cancel-btn', None)):
                user_athlete.workouts_rsvped_for.remove(workout)

    print(Athlete.objects.filter(workouts_rsvped_for=workout))

    # Packaging athletes RSVP'd for this workout
    for item in Athlete.objects.filter(workouts_rsvped_for=workout):
        print(item)

    # Checks if user has already rsvpd
    if (not coach_bool):
        athlete_user = Athlete.objects.get(user=request.user)
        if (athlete_user.workouts_rsvped_for.filter(pk=workout_pk)):
            already_rsvped = True
        else:
            already_rsvped = False


    context = {
        'workout_form': workout_form,
        'workout_team': workout.team,
        'workout_creator': workout.creator,
        'workout_pk': workout.pk,

        'not_creator': not_creator,
        'changed': changed,
        'rsvp_conflict': rsvp_conflict,
        'already_rsvped': already_rsvped
    }

    return render(request, 'workouts/workout-details.html', context)
