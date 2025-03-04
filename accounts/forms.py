from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    """A form for creating users for the custom user model."""

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('first_name','last_name','identity','email','image','line_1','city','state','pincode')
        labels = {'identity':_('Are you a doctor or patient')}
        
class CustomUserChangeForm(UserChangeForm):
    """A form for updating users for the custom user model."""

    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('identity','image','line_1','city','state','pincode')
    