from django import forms
from .models import Event, Attendance, Fee

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location', 'status', 'image']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['user', 'event', 'attended']

class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = ['user', 'amount', 'paid', 'due_date']
