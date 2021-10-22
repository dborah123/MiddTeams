from django import forms
from django.forms.widgets import NumberInput


class WorkoutCreationForm(forms.Form):
    # input fields you want user to input here...some of it can be handled by the view itself
    # so don't worry about covering every field in the Workout model (ie don't worry about 
    # user...we can get that ourselves)
    name = forms.CharField(max_length=120)
    description = forms.CharField(max_length=120)
    date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    time_start = forms.DateTimeField()
    time_end = forms.DateTimeField()
    location = forms.CharField(max_length=120)
 