from django import forms
from django.forms.widgets import NumberInput
from .models import Workout


class WorkoutForm(forms.ModelForm):

    class Meta(object):
        model = Workout

        fields = (
            'name',
            'description',
            'date',
            'time_start',
            'time_end',
            'location',
        )

        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'date': forms.DateInput(
                attrs={
                    'type': 'date',
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
            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

        def __init__(self, *args, **kwargs):
            super(WorkoutForm, self).__init__(*args, **kwargs)
            self.fields['name'].label = ""
            self.fields['description'].label = ""
            self.fields['date'].label = "" 
            self.fields['time_start'].label = ""
            self.fields['time_end'].label = ""
            self.fields['location'].label = "" 
    