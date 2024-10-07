"""
Author: Mussie Abraham
Username/Email: mussieab@bu.edu
Description: This file contains the view for displaying all profiles in the mini_fb application.
"""

from django.shortcuts import render
from django.views.generic import ListView
from .models import Profile

# Create your views here.
class ShowAllProfilesView(ListView):
    """
    A view that displays all profiles in the mini_fb application.

    Attributes:
        model (Profile): The model that this view will display.
        template_name (str): The template used to render the view.
        context_object_name (str): The name of the context object used in the template.
    """
    model = Profile
    template_name = 'mini_fb/show_all_profiles.html'
    context_object_name = 'profiles'