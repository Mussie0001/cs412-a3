from django import forms
from .models import Profile, Comment

class ProfileForm(forms.ModelForm):
    """
    Form for creating or updating a Profile.
    """
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'bio', 'profile_picture_url'] 


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment here...'}),
        }