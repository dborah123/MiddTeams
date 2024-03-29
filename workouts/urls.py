from django.urls import path
from .views import (
    all_workouts,
    home_redirect,
    home_view,
    workout_detail_view
)

app_name='workouts'

urlpatterns = [
    path('', home_redirect, name='home'),
    path('<redirect>', home_view, name='home'),
    path('workout=<pk>/', workout_detail_view, name='workout-detail'),
    path('all-workouts/', all_workouts, name='workout-all'),
]


