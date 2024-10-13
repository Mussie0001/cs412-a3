"""
Author: Mussie Abraham
Username/Email: mussieab@bu.edu
Description: This file contains the URL configuration for the mini_fb application. 
             It maps the root URL to the ShowAllProfilesView.
"""

from django.urls import path
from .views import ShowAllProfilesView, ShowProfilePageView, CreateProfileView, CreateStatusMessageView

urlpatterns = [
    path('', ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'), 
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
]
