from django.db import models
from event_management.models import CustomUser, Event


class Messages(models.Model):
    message = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timeStamp = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, default=1)


