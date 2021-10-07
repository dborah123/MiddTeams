from django import forms


class WorkoutCreationForm(forms.Form):
    # input fields you want user to input here...some of it can be handled by the view itself
    # so don't worry about covering every field in the Workout model (ie...don't worry about 
    # user...we can get that ourselves)