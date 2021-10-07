from django.urls import path
from .views import (
    create_coach_view
)

app_name='workouts'

urlpatterns = [
    path('create-coach/', create_coach_view, name='create_coach'),
]