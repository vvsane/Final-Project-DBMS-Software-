from django.contrib import admin
from .models import Event, Attendance, Fee

# Register your models here.
admin.site.register(Event)
admin.site.register(Attendance)
admin.site.register(Fee)
