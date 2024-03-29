from django import forms
from django.contrib.auth.models import User
from accounts.models import Athlete, Coach, ScheduleItem
from teams.models import Team

DAY_CHOICES = (
    (-1,"Choose..."),
    (0, "Sunday"),
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
)

class CoachCreationForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    password_check = forms.CharField(max_length=200, widget=forms.PasswordInput())
    email = forms.EmailField(max_length=200)
    team = forms.ModelChoiceField(queryset=Team.objects.all())
    formal_title = forms.CharField(max_length=200)
    phone_number = forms.CharField(max_length=200)


class AthleteCreationForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    password_check = forms.CharField(max_length=200, widget=forms.PasswordInput())
    email = forms.EmailField(max_length=200)
    # profile_picture = forms.ImageField()
    team = forms.ModelChoiceField(queryset=Team.objects.all())
    team_code = forms.CharField(max_length=20)
    position = forms.CharField(max_length=200)


class CoachForm(forms.ModelForm):
    # For profiles
    class Meta:
        model = Coach

        fields = (
            'profile_picture',
            'team',
            'formal_title',
            'phone_number',
        )

        exclude = (
            'user',
            'secret_key'
        )

    def __init__(self, *args, **kwargs):
        super(CoachForm, self).__init__(*args, **kwargs)
        self.fields['team'].disabled = True


class AthleteForm(forms.ModelForm):
    # For profiles
    class Meta:
        model = Athlete

        fields = (
            'profile_picture',
            'team',
            'position',
        )

        exclude = (
            'user',
            'secret_key',
        )

    def __init__(self, *args, **kwargs):
        super(AthleteForm, self).__init__(*args, **kwargs)
        self.fields['team'].disabled = True


class UserForm(forms.ModelForm):
    # For profiles
    class Meta:
        model = User

        fields = (
            'email',
            'username',
        )


class PasswordForm(forms.Form):
    # For profiles
    old_password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    new_password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    new_password_again = forms.CharField(max_length=200, widget=forms.PasswordInput())


class ScheduleItemForm(forms.ModelForm):
    # For schedule page
    day = forms.ChoiceField(choices=DAY_CHOICES, widget=forms.Select(attrs={'class':'form-select'}))

    class Meta(object):
        model = ScheduleItem
        fields = (
            'name',
            'time_start',
            'time_end',
            'day',
        )

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'time_start': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': "form-control"
                }
            ),
            'time_end': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': "form-control"
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ScheduleItemForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ""
        self.fields['time_start'].label = ""
        self.fields['time_end'].label = ""
        self.fields['day'].label = "" 

    