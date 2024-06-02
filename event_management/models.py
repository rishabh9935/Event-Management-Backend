from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import date
from cloudinary_storage.storage import RawMediaCloudinaryStorage
from django.contrib.auth.models import PermissionsMixin
from django.utils.timezone import now
from django.contrib.auth.models import User
from .managers import CustomUserManager, EventManager

# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, email, password=None):
#         if not email:
#             raise ValueError("Users must have an email address")
#         if not username:
#             raise ValueError("Users must have a username")

#         user = self.model(
#             email=self.normalize_email(email),
#             username=username,
#         )
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, email, password=None):
#         user = self.create_user(
#             email=self.normalize_email(email),
#             username=username,
#             password=password,
#         )
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
#         user.save(using=self._db)
#         return user


class Donor(models.Model):
    donor_name = models.CharField(max_length=255)
    email = models.EmailField(verbose_name="email", max_length=255, unique=True)

    def __str__(self):
        return self.donor_name


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(verbose_name="email", max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    donor = models.ManyToManyField(Donor, through='DonorManagement', related_name='donors')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
    
    
class AccessAttempt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    first_attempt_time = models.DateTimeField(null=True, blank=True)
    attempt_time = models.DateTimeField(null=True, blank=True)
    login_time = models.DateTimeField(null=True, blank=True)
    logout_time = models.DateTimeField(null=True, blank=True)
    failed_logins = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.login_time if self.login_time else 'Failed Login Attempt'}"
    

class DonorManagement(models.Model):
    donor_id = models.ForeignKey(Donor, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    
# class EventManager(models.Manager):
#     def expired(self):
#         return self.filter(date__lt=now().date())


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField(default=date.today)
    location = models.CharField(max_length=255)
    description = models.TextField()
    details = models.TextField(default='blank')
    is_private = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='event_photos/', storage=RawMediaCloudinaryStorage ,blank=True, null=True)
    role = models.ManyToManyField(CustomUser, through='RoleManagement', related_name='events')
    bidItem = models.CharField(max_length=255, null=True, default=None)
    is_raffle = models.BooleanField(default=False)
    image_urls = models.TextField(blank=True, null=True)

    objects = EventManager()

    def __str__(self):
        return self.name
    

class Role(models.Model):
    ROLE_CHOICES = (
        ('organiser', 'Organiser'),
        ('host', 'Host'),
        ('volunteer', 'Volunteer'),
        ('attending', 'Attending'),
        ('not_attending', 'Not Attending'),
        ('attendees', 'Attendees'),
        ('donor', 'Donor'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.role


class RoleManagement(models.Model):
    event_id=models.ForeignKey(Event,on_delete=models.CASCADE)
    user_id=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    role_id=models.ForeignKey(Role,on_delete=models.CASCADE, null=True)


class Auction(models.Model):
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=10, decimal_places=2)





























# class Organizer(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
    
#     def __str__(self):
#         return f"{self.user.username} - {self.event.name} - {self.role.name}"
    


# class Role(models.Model):
#     name = models.CharField(max_length=100)


# class Ticket(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
#     ticket_type = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

# class Message(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
#     content = models.TextField()
#     timestamp = models.DateTimeField(auto_now_add=True)

# class Feedback(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.CASCADE)
#     attendee = models.ForeignKey(User, on_delete=models.CASCADE)
#     rating = models.IntegerField()
#     comment = models.TextField()

