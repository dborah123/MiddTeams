from django import forms

from accounts.forms import DAY_CHOICES

'''
NOTE: Django won't be able to differentiate from 3 of the same type of forms in one view so I must make 3 seperate
      forms to handle the schedule tool v1
'''

class ScheduleToolForm0(forms.Form):
    time_start0 = forms.TimeField(required=False)
    time_end0 = forms.TimeField(required=False)
    day0 = forms.ChoiceField(choices=DAY_CHOICES, widget=forms.Select(attrs={'class':'form-select'}), required=False)

    time_start0.widget = forms.TimeInput(
        attrs={
            'type': 'time',
            'class':'form-control'
        }
    )
    time_end0.widget = forms.TimeInput(
        attrs={
            'type': 'time',
            'class':'form-control'
        }
    )

class ScheduleToolForm1(forms.Form):
    time_start1 = forms.TimeField(required=False)
    time_end1 = forms.TimeField(required=False)
    day1 = forms.ChoiceField(choices=DAY_CHOICES, widget=forms.Select(attrs={'class':'form-select'}), required=False)

    time_start1.widget = forms.TimeInput(
        attrs={
            'type': 'time',
            'class':'form-control'
        }
    )
    time_end1.widget = forms.TimeInput(
        attrs={
            'type': 'time',
            'class':'form-control'
        }
    )


class ScheduleToolForm2(forms.Form):
    time_start2 = forms.TimeField(required=False)
    time_end2 = forms.TimeField(required=False)
    day2 = forms.ChoiceField(choices=DAY_CHOICES, widget=forms.Select(attrs={'class':'form-select'}), required=False)

    time_start2.widget = forms.TimeInput(
        attrs={
            'type': 'time',
            'class':'form-control'
        }
    )
    time_end2.widget = forms.TimeInput(
        attrs={
            'type': 'time',
            'class':'form-control'
        }
    )

