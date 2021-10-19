from django.urls import path
from .views import (
    create_coach_view,
    create_athlete_view,
    profile_view
)

app_name='workouts'

urlpatterns = [
    path('create-coach/', create_coach_view, name='create_coach'),
    path('create-athlete/', create_athlete_view, name='create_athlete'),
    path('profile/', profile_view, name='profile'),
    # path('profile/schedule/'.)
]