from django.contrib import admin
from .models import Workout, ExcuseRequest

# Register your models here.
admin.site.register(Workout)
admin.site.register(ExcuseRequest)