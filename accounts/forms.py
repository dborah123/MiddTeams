from django import forms
from teams.models import Team

class CoachCreationForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput())
    profile_picture = forms.ImageField()
    email = forms.EmailField(max_length=200)
    team = forms.ModelChoiceField(queryset=Team.objects.all())
    formal_title = forms.CharField(max_length=200)
    phone_number = forms.CharField(max_length=200)


class AthleteCreationForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200)
    profile_picture = forms.ImageField()
    email = forms.EmailField(max_length=200)
    team = forms.ModelChoiceField(queryset=Team.objects.all())
    team_code = forms.CharField(max_length=20)
    phone_number = forms.CharField(max_length=200)

    position = forms.CharField(max_length=200)