from django.db.models.query_utils import Q
from django.shortcuts import redirect, render

from accounts.models import Athlete, Coach, ScheduleItem
from accounts.utils import change_password
from workouts.models import Workout
from .forms import AthleteForm, CoachForm, PasswordForm, ScheduleItemForm, UserForm
from django.contrib.auth.models import User
import json

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def profile_view(request):
    '''
    Redirects user to specific profile page depending other whether they're an athlete or coach
    '''

    # Query if the user is a coach
    is_coach_user = Coach.objects.filter(user=request.user)

    # Redirect user depending on type of user
    if(is_coach_user):
        return coach_profile_view(request)
    else:
        return athlete_profile_view(request)


@login_required(login_url='/login/')
def coach_profile_view(request):
    '''
    Displays coach's profile
    '''
    # Get user and create form
    user = request.user
    user_form = UserForm(request.POST or None, request.FILES or None, instance=user)

    # Get coach and create form
    coach_profile = Coach.objects.get(user=user)
    coach_profile_form = CoachForm(request.POST or None, request.FILES or None, instance=coach_profile)
    profile_changed = 0

    # Create password changing form
    password_form = PasswordForm()
    password_key = -1

    # Change password
    if (request.method == "POST" and "change-password-btn" in request.POST):

        # Get inputs
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password_check = request.POST.get("new_password_check")

        # Verifying new password creation
        password_key = change_password(old_password, 
                                        request.user.password, 
                                        new_password, 
                                        new_password_check
        )

        if (password_key == 0):
            user.password = new_password
            user.save()
    
    # Check is Coach and User forms are valid, save and see if they have changed
    if (coach_profile_form.is_valid()):
        coach_profile_form.save()

        if (coach_profile_form.has_changed()):
            profile_changed = 1
    
    if (user_form.is_valid()):
        user_form.save()

        if (user_form.has_changed()):
            profile_changed = 1

    context = {
        'user_profile':user,
        'user_form':user_form,
        'coach_profile': coach_profile,
        'coach_profile_form': coach_profile_form,
        'profile_changed': profile_changed,
        'password_form':password_form,
        'password_key': password_key,
    }

    return render(request, "accounts/coach-profile.html", context)


@login_required(login_url='/login/')
def athlete_profile_view(request):
    # Get user and create form
    user = request.user
    user_form = UserForm(request.POST or None, request.FILES or None, instance=user)

    # Get athlete and create form
    athlete_profile = Athlete.objects.get(user=request.user)
    athlete_profile_form = AthleteForm(request.POST or None, request.FILES or None, instance=athlete_profile)
    profile_changed = 0

    # Create password changing form
    password_form = PasswordForm()
    password_key = -1

    # Change password
    if(request.method == "POST" and "change-password-btn" in request.POST):

        # Get inputs
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        new_password_check = request.POST.get("new_password_check")

        # Verifying new password creation
        password_key = change_password(old_password, 
                                        request.user.password, 
                                        new_password, 
                                        new_password_check
        )

        if (password_key == 0):
            user.password = new_password
            user.save()
    else:
        #Validate and save any changes to Athlete
        if (athlete_profile_form.is_valid()):
            athlete_profile_form.save()

            if (athlete_profile_form.has_changed()):
                profile_changed = 1

        #Validate and save any changes to User
        if (user_form.is_valid()):
            user_form.save()

            if (user_form.has_changed()):
                profile_changed = 1

    context = {
        'user_profile':user,
        'user_form':user_form,
        'profile_changed': profile_changed,
        'athlete_profile': athlete_profile,
        'athlete_profile_form': athlete_profile_form,
        "password_form": password_form,
        "password_key": password_key,
    }

    return render(request, "accounts/athlete-profile.html", context)


@login_required(login_url='/login/')
def schedule_view(request, **kwargs):
    """
    Collects schedule of Athlete designated by pk and passes it to js, displaying schedule
    """
    # Get pk and user (owner of schedule)
    user_pk = kwargs.get('pk')
    user = User.objects.get(pk=user_pk)

    # Check if actual user is owner of this schedule as it determines permissions
    if (request.user.pk != user.pk):
        not_owner = True
        schedule_item_form = None
    else:
        schedule_item_form = ScheduleItemForm(request.POST or None)
        not_owner = False

    # Initialize schedule form
    schedule_data = []
    already_exists = 0

    # Handle ScheduleItem creation
    if (request.method == "POST" 
        and schedule_item_form.is_valid() 
        and request.POST.get("submit")):

        schedule_item = schedule_item_form.save(commit=False)
        schedule_item.user = user

        # Check if there is conflicting items or form isn't valid
        if (schedule_item.not_valid() or 
            ScheduleItem.objects.filter(
                Q(time_start__range=[schedule_item.time_start, schedule_item.time_end], day=schedule_item.day, user=user) |
                Q(time_end__range=[schedule_item.time_start, schedule_item.time_end], day=schedule_item.day, user=user) |
                Q(time_start__lte=schedule_item.time_start, time_end__gte=schedule_item.time_end, day=schedule_item.day, user=user)
            )):
            already_exists = 1
        else:
            already_exists = 2
            schedule_item.save()

        # Reset form
        schedule_item_form = ScheduleItemForm()


    # Getting data for schedule in two parts: schedule items (ie classes) and workouts scheduled

    # Querying all ScheduleItems in the database connected to the current user
    schedule_items = ScheduleItem.objects.filter(user=user)

    # Append schedule items to specific day
    for item in schedule_items:
        url_string = f"/accounts/profile/schedule/user={user_pk}/{item.pk}"
        data = {
            'title': item.name,
            'startTime': item.time_start.strftime("%H:%M"),
            'endTime': item.time_end.strftime("%H:%M"),
            'daysOfWeek': [item.day],
            'startReoccur': '2020-9-9',
            'endReoccur': '2020-14-12',
            'url': url_string,
        }
        schedule_data.append(data)

    # Packaging data about workouts
    if (Coach.objects.filter(user=user)):
        coach = Coach.objects.get(user=user)
        for item in Workout.objects.filter(team=coach.team):
            url_string = f"/workout={item.pk}"
            data = {
                'title': item.name,
                'start': str(item.date) + "T" + item.time_end.strftime("%H:%M"),
                'end': str(item.date) + "T" + item.time_end.strftime("%H:%M"),
                'url': url_string,
            }
            schedule_data.append(data)

    else:
        athlete = Athlete.objects.get(user=user)
        for item in athlete.workouts_rsvped_for.all():
            url_string = f"/workout={item.pk}"
            data = {
                'title': item.name,
                'start': str(item.date) + "T" + item.time_end.strftime("%H:%M"),
                'end': str(item.date) + "T" + item.time_end.strftime("%H:%M"),
                'url': url_string,
            }
            schedule_data.append(data)

    context = {
        'user_first_name':user.first_name,
        'schedule_data': json.dumps(schedule_data),
        'schedule_item_form': schedule_item_form,
        'already_exists': already_exists,
        'not_owner': not_owner,
    }

    return render(request, 'accounts/schedule.html', context)


@login_required(login_url='/login/')
def schedule_item_view(request, **kwargs):
    '''
    Displays specific schedule item to user with capability to update and delete
    '''
    # Initialize user variables
    user = request.user
    user_pk = kwargs.get('pk')

    changed = 0

    # Verify that user is ower of schedule item
    if (user.pk != int(user_pk)):
        return redirect(f'/accounts/profile/schedule/user={user_pk}') 

    # Get schedule item
    schedule_id = kwargs.get('sid')
    schedule_item = ScheduleItem.objects.get(pk=schedule_id)

    # Creating schedule form
    schedule_item_form = ScheduleItemForm(request.POST or None,
                                          request.FILES or None,
                                          instance=schedule_item)

    # Save changes
    if (schedule_item_form.is_valid() and 
        ScheduleItem.objects.filter(
                Q(time_start__range=[schedule_item.time_start, schedule_item.time_end], day=schedule_item.day, user=user) |
                Q(time_end__range=[schedule_item.time_start, schedule_item.time_end], day=schedule_item.day, user=user) |
                Q(time_start__lte=schedule_item.time_start, time_end__gte=schedule_item.time_end, day=schedule_item.day, user=user)
    )):
        schedule_item_form.save()

        if(schedule_item_form.has_changed()):
            changed = 1
    
    # Delete item
    if (request.method == "POST" and request.POST.get('delete')):
        schedule_item.delete()
        return redirect(f'/accounts/profile/schedule/user={user_pk}')

    context = {
        'schedule_item': schedule_item,
        'schedule_item_form': schedule_item_form,
        'changed': changed,
        'user_pk': user.pk,
    }

    return render(request, 'accounts/schedule-item.html', context)
