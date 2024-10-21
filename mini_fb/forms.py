from django import forms
from .models import Profile, StatusMessage

class CreateProfileForm(forms.ModelForm):
    """
    This form will allow users to input their first name, last name, city, email, and profile image URL for a new Profile object.
    """

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'city', 'email', 'profile_image_url']


class CreateStatusMessageForm(forms.ModelForm):
    """
    A form for creating a new status message.
    """

    class Meta:
        model = StatusMessage
        fields = ['message']

class UpdateProfileForm(forms.ModelForm):
    """
    A form for updating an existing Profile object.
    
    Only allows updating certain fields, not the first name or last name.
    """

    class Meta:
        model = Profile
        fields = ['city', 'email', 'profile_image_url']
