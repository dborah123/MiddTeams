from django.urls import path

from teams.views import excuses_view, roster_view, schedule_tool

app_name = 'teams'

urlpatterns = [
    path('roster/', roster_view, name='roster'),
    path('schedule-tool/', schedule_tool, name='schedule-tool'),
    path('excuses/', excuses_view, name="excuses")
]