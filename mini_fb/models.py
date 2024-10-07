"""
Author: Mussie Abraham
Username/Email: mussieab@bu.edu
Description: This file contains the model definitions for the mini Facebook application.
"""

from django.db import models

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

        Returns:
            str: The full name of the user.
        """
        return f"{self.first_name} {self.last_name}"