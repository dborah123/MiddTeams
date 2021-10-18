from django import forms
from django.contrib.auth import models
from accounts.models import Coach
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
    email = forms.EmailField(max_length=200)
    profile_picture = forms.ImageField()
    team = forms.ModelChoiceField(queryset=Team.objects.all())
    team_code = forms.CharField(max_length=20)
    position = forms.CharField(max_length=200)

class CoachForm(forms.ModelForm):
    class Meta:
        model = Coach
        exclude = (
            'user',
            'secret_key'
        )