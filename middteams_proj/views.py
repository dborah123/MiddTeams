from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import Coach, Athlete
from accounts.forms import CoachCreationForm, AthleteCreationForm
from teams.models import Team

def logout_view(request):
    '''
    handles logout
    '''

    logout(request)
    return redirect('login')


def login_view(request):
    '''
    handles login
    '''
    # Forms
    login_form = AuthenticationForm()
    coach_create_form = CoachCreationForm()
    athlete_create_form = AthleteCreationForm()

    # Message variables
    error_message = 0
    email_taken = 0
    password_match = 0
    account_created = 0
    wrong_team_code = 0


    # Athlete creation variable initialization

    if(request.method == 'POST'):

        #LOGIN LOGIC
        if (request.POST.get("login")):
            form = AuthenticationForm(data=request.POST)

            if(form.is_valid()):
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)

                if(user is not None):
                    login(request, user)
                    
                    if(request.GET.get('next')):
                        return redirect(request.GET.get('next'))
                    else:
                        # Brings user to homepage
                        return redirect('workouts:home')
            else:
                error_message = 1

        # COACH CREATION LOGIC
        elif (request.POST.get("create-coach")):

                # Checking if passwords match
                password = request.POST.get("password")
                password_check = request.POST.get("password_check")

                if(password != password_check):
                    password_match = 1

                # Creating user model
                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")

                email = request.POST.get("email")

                # Check if email is already taken
                if(User.objects.filter(email=email)):
                    email_taken = 1
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
                    account_created = 1
   
        # ATHLETE CREATION LOGIC
        elif (request.POST.get("create-athlete")):

            # Verifying team code to add them to roster
            team_code = request.POST.get("team_code")
            team = Team.objects.get(pk=request.POST.get("team"))

            # Getting passwords to check if they match
            password = request.POST.get("password")
            password_check = request.POST.get("password_check")

            if(team_code != team.team_code):
                wrong_team_code = 1
            
            elif(password != password_check):
                password_match = 1

            else:
                #Creating user model
                first_name = request.POST.get("first_name")
                last_name = request.POST.get("last_name")

                email = request.POST.get("email")

                # Check if email is already taken
                if(User.objects.filter(email=email)):
                    email_taken = 1
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
                    account_created = 1



    context = {
        'form':login_form,
        'error_message': error_message,

        'coach_creation_form': coach_create_form,
        'athlete_create_form': athlete_create_form,

        'email_taken': email_taken,
        'password_match': password_match,
        'account_created': account_created,
        'wrong_team_code': wrong_team_code,
    }

    return render(request, 'auth/login.html', context)