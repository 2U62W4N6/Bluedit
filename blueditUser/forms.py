from django import forms
from .models import BlueditUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class EditBio(forms.ModelForm):
    class Meta:
        model = BlueditUser
        fields = ['profilePicture', 'bio']
        widgets = {
            'user': forms.HiddenInput(),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = BlueditUser
        fields = ('username',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = BlueditUser
        fields = ('bio', 'profilePicture')