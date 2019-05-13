from django.db import models
from django.conf import settings
from django.utils import timezone

class Ticket(models.Model):
    title = models.CharField(max_length=254, default="") #check for default value
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    dateTime = models.DateTimeField(default=timezone.now)
    lastUpdate = models.DateTimeField(auto_now=True)

    States = (
        ('Waiting for response', 'Waiting for response'),
        ('Answered', 'Answered'),
        ('Closed', 'Closed'),
    )
    state = models.CharField(max_length=20, choices=States, default="Waiting for response")

    Priorities = (
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    )
    priority = models.CharField(max_length=6, choices=Priorities, default=0)

    def __str__(self):
        return self.title

class Comment(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    from_owner = models.BooleanField(default=True)
    comment = models.TextField(blank=False, default="")
    dateTime = models.DateTimeField(auto_now=True)