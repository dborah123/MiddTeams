from django.urls import path

from teams.views import schedule_tool_v2_view, absences_view, roster_view, schedule_tool

app_name = 'teams'

urlpatterns = [
    path('roster/', roster_view, name='roster'),
    path('schedule-tool/', schedule_tool, name='schedule-tool'),
    path('absences/', absences_view, name="absences"),
    path('schedule-toolv2/', schedule_tool_v2_view, name="schedule-tool-v2"),
]