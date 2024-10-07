"""
Author: Mussie Abraham
Username/Email: mussieab@bu.edu
Description: This file contains the URL configuration for the mini_fb application. 
             It maps the root URL to the ShowAllProfilesView.
"""

from django.urls import path
from .views import ShowAllProfilesView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
]
