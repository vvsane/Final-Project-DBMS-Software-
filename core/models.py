from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Event(models.Model):
    STATUS_CHOICES=[
        ('ongoing', 'Ongoing'),
        ('done', 'Done'),
        ('postponed', 'Postponed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    status = models.CharField(
        max_length=100, 
        choices=STATUS_CHOICES,
        blank=True,
        null=True,
    )
    
    def get_status(self):
        if self.status == 'postponed':
            return 'Postponed'
        elif self.status:
            return self.get_status_display() 
        elif self.date > timezone.now():
            return 'Ongoing'
        else:
            return 'Done'

    def __str__(self):
        return f"{self.title} - {self.get_status()}"

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"

class Fee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid = models.BooleanField(default=False)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.user.username}"
