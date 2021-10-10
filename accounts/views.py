from django.shortcuts import render

from accounts.models import Coach
from .forms import CoachCreationForm, AthleteCreationForm
from django.contrib.auth.models import User

# Create your views here.

def create_coach_view(request):
    coach_create_form = CoachCreationForm()
    email_taken = False

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

            Coach.objects.create(
                                    user=user,
                                    profile_picture=profile_pic,
                                    team=team,
                                    formal_title=formal_title,
                                    phone_number=phone_number
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

    context = {
        'email_taken':email_taken,
        'athlete_create_form':athlete_create_form
    }

    return render(request, 'accounts/create-athlete.html', context)