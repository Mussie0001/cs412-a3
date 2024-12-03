from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    """
    Form for creating or updating a Profile.
    """
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'profile_picture_url'] 


