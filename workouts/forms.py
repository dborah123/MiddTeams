from django import forms
from django.forms.widgets import NumberInput
from .models import Workout


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
            super(Workout, self).__init__(*args, **kwargs)
            self.fields['name'].label = ""
            self.fields['description'].label = ""
            self.fields['date'].label = "" 
            self.fields['time_start'].label = ""
            self.fields['time_end'].label = ""
            self.fields['location'].label = "" 
    