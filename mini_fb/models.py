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
    
    def get_friends(self):
        """
        Returns all profiles that are friends with this profile.
        """
        friends_as_profile1 = Friend.objects.filter(profile1=self)
        friends_as_profile2 = Friend.objects.filter(profile2=self)

        friends = [friend.profile2 for friend in friends_as_profile1]
        friends += [friend.profile1 for friend in friends_as_profile2]  

        return friends
    
    def get_friend_suggestions(self):
        """
        Returns a list of profiles that are not currently friends with this profile
        and does not include this profile itself.
        """
        current_friends = set(self.get_friends())
        suggested_friends = Profile.objects.exclude(pk=self.pk).exclude(pk__in=[friend.pk for friend in current_friends])

        return suggested_friends
    
    def add_friend(self, other):
        """
        Adds a friend relation between this profile and the other profile & prevents duplicate friendships and self-friending.
        """
        if self == other:
            raise ValueError("Cannot add self as a friend.")

        friend_exists = Friend.objects.filter(
            models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)
        ).exists()

        if not friend_exists:
            friend = Friend(profile1=self, profile2=other)
            friend.save()

    def get_news_feed(self):
        """
        Returns a QuerySet of all status messages from this profile and their friends,
        sorted by the most recent first.
        """
        own_statuses = StatusMessage.objects.filter(profile=self)
        friends = self.get_friends() 
        friends_statuses = StatusMessage.objects.filter(profile__in=friends)
        news_feed = own_statuses.union(friends_statuses).order_by('-timestamp')

        return news_feed
    
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

    def get_images(self):
        """
        Returns all images associated with this StatusMessage.
        """
        return self.images.all()

    def __str__(self):
        """
        Returns a string representation of the StatusMessage instance.
        """
        return f"Message by {self.profile.first_name} on {self.timestamp}: {self.message[:30]}"
    
class Image(models.Model):
    """
    A model representing an image uploaded for a status message.

    Attributes:
        image_file (File): The actual image file uploaded.
        timestamp (datetime): The time the image was uploaded.
        status_message (StatusMessage): The status message this image is related to.
    """
    image_file = models.ImageField(upload_to='images/')
    timestamp = models.DateTimeField(default=timezone.now)
    status_message = models.ForeignKey(StatusMessage, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        """
        Returns a string representation of the Image instance.
        """
        return f"Image for {self.status_message.message[:30]} uploaded at {self.timestamp}"
    
class Friend(models.Model):
    """
    A model representing a friendship between two profiles that are friends with each other.
    Attributes:
        profile1 (ForeignKey): The first profile in the friendship.
        profile2 (ForeignKey): The second profile in the friendship.
        timestamp (DateTimeField): The date when the friendship was created.
    """
    profile1 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile1")
    profile2 = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="profile2")
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        """
        Returns a string representation of the friendship, including both profiles' names.
        """
        return f"{self.profile1.first_name} {self.profile1.last_name} & {self.profile2.first_name} {self.profile2.last_name}"