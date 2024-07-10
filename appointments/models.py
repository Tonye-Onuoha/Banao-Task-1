from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Calendar(models.Model):
    """This class represents a Calendar Model"""
    
    specialty = models.CharField(max_length=100, help_text='Enter your required specialty')
    date = models.DateField(help_text="Enter your appointment date", null=True, blank=False)
    start_time = models.TimeField(help_text="Enter your appointment time", null=True, blank=False)
    end_time = models.TimeField(null=True, blank=False)
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='doctor_calendar_set')
    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='patient_calendar_set')
    
    class Meta:
        ordering = ['id']
        
    def __str__(self):
        return f'{self.patient.first_name} {self.patient.last_name}\'s {self.specialty} appointment'
