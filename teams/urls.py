from django.urls import path

from teams.views import roster_view

app_name = 'teams'

urlpatterns = [
    path('roster', roster_view, name='roster'),
]