from django.urls import path
from .views import (
    profile_view,
    schedule_view,
    schedule_item_view,
)

app_name='accounts'

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('profile/schedule/user=<pk>', schedule_view, name='schedule'),
    path('profile/schedule/user=<pk>/<sid>', schedule_item_view, name='schedule-item'),
]