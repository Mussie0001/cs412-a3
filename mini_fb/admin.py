"""
Author: Mussie Abraham
Username/Email: mussieab@bu.edu
Description: This file registers the Profile model with the Django admin site.
"""
from django.contrib import admin
from .models import Profile, StatusMessage, Image, Friend

# Register your models here.
admin.site.register(Profile)
admin.site.register(StatusMessage)
admin.site.register(Image)
admin.site.register(Friend)
