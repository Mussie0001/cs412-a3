"""
Author: Mussie Abraham
Username/Email: mussieab@bu.edu
Description: This file contains the model definitions for the mini Facebook application.
"""

from django.db import models
from django.utils import timezone
from django.urls import reverse

class Profile(models.Model):
    """
    A model representing a user profile.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        city (str): The city where the user resides.
        email (str): The email address of the user, must be unique.
        profile_image_url (str): The URL of the user's profile image.
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    city = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    profile_image_url = models.URLField(max_length=200)

    def __str__(self):
        """
        Returns a string representation of the Profile instance.
        """
        return f"{self.first_name} {self.last_name}"
    
    def get_status_messages(self):
        """
        Returns all status messages related to this profile, ordered by timestamp.
        """
        return self.status_messages.all().order_by('-timestamp')
    
    def get_absolute_url(self):
        """
        Returns the URL to view this Profile object.
        """
        return reverse('show_profile', kwargs={'pk': self.pk})
    
class StatusMessage(models.Model):
    """
    A model representing a Facebook-style status message.

    Attributes:
        timestamp (datetime): The time the status message was created.
        message (str): The content of the status message.
        profile (Profile): The profile of the user who created the status message.
    """
    timestamp = models.DateTimeField(default=timezone.now)
    message = models.TextField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='status_messages')

    def __str__(self):
        """
        Returns a string representation of the StatusMessage instance.
        """
        return f"Message by {self.profile.first_name} on {self.timestamp}: {self.message[:30]}"