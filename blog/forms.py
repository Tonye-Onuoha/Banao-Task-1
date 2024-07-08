from django import forms
from .models import Post
from django.utils.translation import gettext_lazy as _

class PostModelForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title','image','category','summary','content','is_draft']
        labels = {'is_draft':_('mark as draft')}