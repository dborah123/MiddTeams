from django import forms
from django.forms import fields
from django.forms import widgets
from django.forms.widgets import NumberInput
from .models import EXCUSE_OPTIONS, ExcuseRequest, Workout


class WorkoutCreationForm(forms.ModelForm):

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
            'description': forms.Textarea(
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
        super(WorkoutCreationForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ""
        self.fields['description'].label = ""
        self.fields['date'].label = "" 
        self.fields['time_start'].label = ""
        self.fields['time_end'].label = ""
        self.fields['location'].label = "" 


class WorkoutForm(forms.ModelForm):

    class Meta(object):
        model = Workout

        fields = (
            'name',
            'description',
            'team',
            'creator',
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
            'description': forms.Textarea(
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
            'team': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'creator': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

    def __init__(self, *args, disable_fields=False, **kwargs):
        super(WorkoutForm, self).__init__(*args, **kwargs)
        self.fields['team'].disabled = True
        self.fields['creator'].disabled = True

        if (disable_fields):
            self.fields['name'].disabled = True            
            self.fields['description'].disabled = True
            self.fields['date'].disabled = True
            self.fields['time_start'].disabled = True
            self.fields['time_end'].disabled = True
            self.fields['location'].disabled = True


class ExcuseForm(forms.ModelForm):

    reason = forms.ChoiceField(choices=EXCUSE_OPTIONS, widget=forms.Select(attrs={'class':'form-select'}))

    class Meta:
        model = ExcuseRequest

        fields = (
            'reason',
            'explanation',
        )

        widgets = {
            'explanation': forms.Textarea(
                attrs={
                    'class':'form-control',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(ExcuseForm, self).__init__(*args, **kwargs)
        self.fields['explanation'].label=""
    
