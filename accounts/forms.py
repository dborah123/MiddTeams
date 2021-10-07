from django import forms
from django.db import models
from teams.models import Team

class CoachCreationForm(forms.Form):
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)
    profile_picture = forms.ImageField()
    email = forms.EmailField(max_length=200)
    team = forms.ModelChoiceField(queryset=Team.objects.all())
    formal_title = forms.CharField(max_length=200)
    phone_number = forms.CharField(max_length=200)

    coach_key = forms.CharField(max_length=200)