from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Links to the built-in User
    age = models.PositiveIntegerField(blank=True, null=True)  # Age (positive number, optional)
    address = models.TextField(blank=True)  # Address (multi-line text, optional)
    telephone = models.CharField(max_length=20, blank=True)  # Phone number (string, optional)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)  # Gender dropdown
    occupation = models.CharField(max_length=100, blank=True)  # Occupation (short text, optional)

    def __str__(self):
        return f"{self.user.username}'s Profile"
