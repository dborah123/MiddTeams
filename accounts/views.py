from django.db.models.query_utils import Q
from django.shortcuts import redirect, render

from accounts.models import Athlete, Coach, ScheduleItem
from accounts.utils import change_password
from teams.models import Team
from .forms import AthleteForm, CoachCreationForm, AthleteCreationForm, CoachForm, PasswordForm, ScheduleItemForm, UserForm
from django.contrib.auth.models import User
import json

# Create your views here.
def create_coach_view(request):
    coach_create_form = CoachCreationForm()
    email_taken = False
    password_match = True

    # If user submitted form
    if(request.method == "POST"):

        # Checking if passwords match
        password = request.POST.get("password")
        password_check = request.POST.get("password_check")

        if(password != password_check):
            password_match = False

        # Creating user model
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        email = request.POST.get("email")

        # Check if email is already taken
        if(User.objects.filter(email=email)):
            email_taken = True
        else:
            user = User.objects.create_user(
                                            first_name=first_name, 
                                            last_name=last_name, 
                                            username=email.split('@')[0],
                                            password=password, 
                                            email=email
                                            )

            # Creating coach model
            profile_pic = request.POST.get("profile_picture")
            team = request.POST.get("team")
            formal_title = request.POST.get("formal_title")
            phone_number = request.POST.get("phone_number")
            Coach.objects.create(
                                    user=user,
                                    profile_picture=profile_pic,
                                    team=Team.objects.get(pk=team),
                                    formal_title=formal_title,
                                    phone_number=phone_number,
                                )
            # TODO: render login page here


    context = {
        'coach_create_form':coach_create_form,
        'password_match': password_match,
        'email_taken':email_taken,
    }

    return render(request, 'accounts/create-coach.html', context)


def create_athlete_view(request):
    athlete_create_form = AthleteCreationForm()
    email_taken = False
    wrong_team_code = False
    password_match = True

    # If user submitted form
    if(request.method == "POST"):

        # Verifying team code to add them to roster
        team_code = request.POST.get("team_code")
        team = Team.objects.get(pk=request.POST.get("team"))

        # Getting passwords to check if they match
        password = request.POST.get("password")
        password_check = request.POST.get("password_check")

        if(team_code != team.team_code):
            wrong_team_code = True
        
        elif(password != password_check):
            password_match = False

        else:
            #Creating user model
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")

            email = request.POST.get("email")

            # Check if email is already taken
            if(User.objects.filter(email=email)):
                email_taken = True
            else:
                user = User.objects.create_user(
                                                first_name=first_name, 
                                                last_name=last_name, 
                                                username=email.split('@')[0],
                                                password=password, 
                                                email=email
                                                )

                #Creating Athlete model object
                profile_pic = request.POST.get("profile_picture")
                position = request.POST.get("position")

                Athlete.objects.create(
                                        user=user,
                                        profile_picture=profile_pic,
                                        team=team,
                                        position=position,
                                        )

                # TODO: render login page here

    context = {
        'athlete_create_form':athlete_create_form,
        'password_match':password_match,
        'email_taken':email_taken,
        'wrong_team_code':wrong_team_code,
    }

    return render(request, 'accounts/create-athlete.html', context)


def profile_view(request):

    # Query if the user is a coach
    is_coach_user = Coach.objects.get(user=request.user)

    # Redirect user depending on type of user
    if(is_coach_user):
        return coach_profile_view(request)
    else:
        return athlete_profile_view(request)


def coach_profile_view(request):

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


def athlete_profile_view(request):

    # Get user and create form
    user = request.user
    user_form = UserForm(request.POST or None, request.FILES or None, instance=user)

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
        'profile_changed': profile_changed,
        'athlete_profile': athlete_profile,
        'athlete_profile_form': athlete_profile_form,
        "password_form": password_form,
        "password_key": password_key,
    }

    return render(request, "accounts/athlete-profile.html", context)


def schedule_view(request, **kwargs):
    """
    Collects schedule of Athlete designated by pk and passes it to js, displaying schedule
    """

    # Get pk and user
    pk = kwargs.get('pk')
    user = User.objects.get(pk=pk)

    schedule_item_form = ScheduleItemForm(request.POST or None)

    schedule_data = []

    already_exists = 0

    # LOOK HERE FOR HOW TO SAVE
    if(request.method == "POST" 
        and schedule_item_form.is_valid() 
        and request.POST.get("submit")):

        schedule_item = schedule_item_form.save(commit=False)
        schedule_item.user = user

        # VALID IS A FUNCTION IN MODELS THAT VALIDATES IF THAT MODEL OBJECT IS VALID...CREATE THIS FOR WORKOUTS
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

        schedule_item_form = ScheduleItemForm()


    # Getting data for schedule in two parts: schedule items (ie classes) and workouts scheduled

    # Getting ScheduleItems

    # Querying all ScheduleItems in the database
    schedule_items = ScheduleItem.objects.filter(user=user)

    # Append schedule items to specific day
    for item in schedule_items:
        url_string = f"/accounts/profile/schedule/user={user.pk}/{item.pk}"
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

    context = {
        'user_first_name':user.first_name,
        'schedule_data': schedule_data,
        'schedule_item_form': schedule_item_form,
        'already_exists': already_exists,
    }

    context['schedule_data'] = json.dumps(context['schedule_data'])

    return render(request, 'accounts/schedule.html', context)


def schedule_item_view(request, **kwargs):

    # Initialize random variables
    changed = 0
    user_pk = kwargs.get('pk')
    user = User.objects.get(pk=user_pk)

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
        'user_pk': user_pk,
    }

    return render(request, 'accounts/schedule-item.html', context)
