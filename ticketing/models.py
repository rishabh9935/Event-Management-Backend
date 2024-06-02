from django.db import models
from event_management.models import Event, CustomUser


class TicketType(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.event.name}"
    
    # class Meta:
    #     unique_together = ('name', 'price', 'event')


class Ticket(models.Model):
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE)
    qr_code = models.ImageField(upload_to="ticket_qr/", blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    checked_in = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.ticket_type.event.name}"
    

