from django.shortcuts import render

from accounts.models import Athlete, Coach
from teams.models import Team
from .forms import CoachCreationForm, AthleteCreationForm
from django.contrib.auth.models import User

# Create your views here.
def create_coach_view(request):
    coach_create_form = CoachCreationForm()
    email_taken = False


    # If user submitted form
    if(request.method == "POST"):

        # Creating user model
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check if email is already taken
        if(User.objects.filter(email=email)):
            email_taken = True
        else:
            user = User.objects.create_user(
                                            first_name=first_name, 
                                            last_name=last_name, 
                                            username=email,
                                            password=password, 
                                            email=email
                                            )

            # Creating coach model
            profile_pic = request.POST.get("profile_picture")
            team = request.POST.get("team")
            formal_title = request.POST.get("formal_title")
            phone_number = request.POST.get("phone_number")
            print("creating object")
            Coach.objects.create(
                                    user=user,
                                    profile_picture=profile_pic,
                                    team=Team.objects.get(pk=team),
                                    formal_title=formal_title,
                                    phone_number=phone_number,
                                )
            # TODO: render login page here


    context = {
        'email_taken':email_taken,
        'coach_create_form':coach_create_form,
    }

    return render(request, 'accounts/create-coach.html', context)


def create_athlete_view(request):
    athlete_create_form = AthleteCreationForm()
    email_taken = False
    wrong_team_code = False

    # If user submitted form
    if(request.method == "POST"):

        # Verifying team code to add them to roster
        team_code = request.POST.get("team_code")
        team = Team.objects.get(pk=request.POST.get("team"))

        if(team_code != team.team_code):
            wrong_team_code = True
            print("here")

        else:
            #Creating user model
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")

            email = request.POST.get("email")
            password = request.POST.get("password")

            # Check if email is already taken
            if(User.objects.filter(email=email)):
                print("email is taken")
                email_taken = True
            else:
                print("email isnt taken")
                user = User.objects.create_user(
                                                first_name=first_name, 
                                                last_name=last_name, 
                                                username=email,
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
        'email_taken':email_taken,
        'athlete_create_form':athlete_create_form,
        'wrong_team_code':wrong_team_code,
    }

    return render(request, 'accounts/create-athlete.html', context)