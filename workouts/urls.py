from django.urls import path
from .views import (
    home_view,
    workout_detail_view
)

app_name='workouts'

urlpatterns = [
    path('', home_view, name='home'),
    path('workout=<pk>/', workout_detail_view, name='workout-detail'),
]


