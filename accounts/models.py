from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from PIL import Image

# Create your models here.
class CustomUser(AbstractUser):
    IDENTITY_CHOICES = [("DC", "Doctor"),("PT", "Patient")]
    identity = models.CharField(max_length=2,choices=IDENTITY_CHOICES,default="DC")
    image = models.ImageField(upload_to='profile_pics')
    line_1 = models.CharField(max_length=100,help_text='Enter your house address')
    city = models.CharField(max_length=100,help_text='Enter your city')
    state = models.CharField(max_length=100,help_text='Enter your state')
    pincode = models.PositiveIntegerField(help_text='Enter your pincode',blank=False,null=True)
    
    def __str__(self):
        return f'{self.username}'
        
        
    
