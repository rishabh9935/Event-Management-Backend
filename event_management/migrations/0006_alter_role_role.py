# Generated by Django 5.0.4 on 2024-04-22 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event_management', '0005_event_biditem_event_is_raffle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='role',
            field=models.CharField(choices=[('organiser', 'Organiser'), ('host', 'Host'), ('volunteer', 'Volunteer'), ('attending', 'Attending'), ('not_attending', 'Not Attending'), ('attendees', 'Attendees'), ('donor', 'Donor')], max_length=20),
        ),
    ]
