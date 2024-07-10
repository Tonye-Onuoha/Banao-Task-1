from django import forms
from django.forms import DateInput, TimeInput
from .models import Calendar
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import datetime

class CalendarModelForm(forms.ModelForm):
    
    class Meta:
        model = Calendar
        fields = ['specialty', 'date', 'start_time']
        labels ={'specialty':_('Required specialty'),'date':_('Date of Appointment'), 'start_time':_('Start Time of Appointment')}
        widgets = {'date': DateInput(attrs={'placeholder':'YY-M-D', 'type': 'date'}), 'start_time': TimeInput(attrs={'placeholder':'HH:MM', 'type':'time'})}
        
        #add the following attribute to include date-picker:
        #'type': 'date'
        
    def clean_date(self):
        data = self.cleaned_data['date']

        # Check if a date is not in the past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - appoinment date is set in the past'))

        # Remember to always return the cleaned data.
        return data