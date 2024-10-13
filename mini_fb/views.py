"""
Author: Mussie Abraham
Username/Email: mussieab@bu.edu
Description: This file contains the view for displaying all profiles in the mini_fb application.
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Profile, StatusMessage
from .forms import CreateProfileForm, CreateStatusMessageForm
from django.urls import reverse



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

class ShowProfilePageView(DetailView):
    """
    A view that displays a single profile in the mini_fb application.

    Attributes:
        model (Profile): The model that this view will display.
        template_name (str): The template used to render the view.
        context_object_name (str): The name of the context object used in the template.
    """
    model = Profile
    template_name = 'mini_fb/show_profile.html'
    context_object_name = 'profile'


class CreateProfileView(CreateView):
    """
    A view that handles creating a new Profile.

    This view uses the CreateProfileForm to allow users to create a new profile.
    """
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        """
        Returns the URL to redirect to after successfully creating a profile.
        """
        return reverse('show_profile', kwargs={'pk': self.object.pk})


class CreateStatusMessageView(CreateView):
    """
    A view to handle the creation of a new status message for a profile.
    """
    model = StatusMessage
    form_class = CreateStatusMessageForm
    template_name = 'mini_fb/create_status_form.html'

    def get_context_data(self, **kwargs):
        """
        Adds the Profile object to the context for the form.
        """
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        """
        Sets the profile attribute of the StatusMessage before saving.
        """
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile
        return super().form_valid(form)

    def get_success_url(self):
        """
        Returns the URL to redirect to after the form is successfully submitted.
        """
        return reverse('show_profile', kwargs={'pk': self.kwargs['pk']})