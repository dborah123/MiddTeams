from django import forms
from .models import ABSENCE_OPTIONS, ExcuseRequest, Workout


class WorkoutCreationForm(forms.ModelForm):
    '''
    Form for creating workouts
    '''
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
    '''
    Form for displaying and editing already created workouts
    '''
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
        # NOTE: Depending on user permissions (whether they are owner/coach), fields could be disabled
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


class AbsenceForm(forms.ModelForm):
    '''
    Form for filling out an absences
    '''
    reason = forms.ChoiceField(choices=ABSENCE_OPTIONS, widget=forms.Select(attrs={'class':'form-select'}))

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
        super(AbsenceForm, self).__init__(*args, **kwargs)
        self.fields['explanation'].label=""
    
