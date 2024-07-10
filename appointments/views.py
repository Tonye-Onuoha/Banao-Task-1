from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import CalendarModelForm
from accounts.models import CustomUser
from .models import Calendar
from django.contrib.auth.decorators import login_required
from datetime import datetime, time, timedelta
import os.path
# Google imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


# Create your views here.
@login_required
def create_appointment(request, pk):
    """This view renders a form that patients use to book appointments with doctors."""
    
    doctor = get_object_or_404(CustomUser, id=pk)

    if request.method == 'POST':
        form = CalendarModelForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data.get('date')
            start_time = form.cleaned_data.get('start_time')
            full_date = datetime(year=date.year,month=date.month,day=date.day,hour=start_time.hour,minute=start_time.minute,second=0)
            appointment_duration = timedelta(minutes=45, seconds=0)
            full_endtime = full_date + appointment_duration
            end_time = time(hour=full_endtime.hour,minute=full_endtime.minute,second=full_endtime.second)
            appointment = form.save(commit=False)
            appointment.end_time = end_time
            appointment.doctor = doctor
            appointment.patient = request.user
            appointment.save()
            
            # Google Calendar API code here:
            
            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)
                
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                    creds = flow.run_local_server(port=0)
                # Save the credentials for the next run.
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
                    
                    
            try:
                service = build("calendar", "v3", credentials=creds)
                
                # Create calendar event.
                summary = appointment.specialty
                date = date.strftime('%Y-%m-%d')
                start_datetime = full_date.isoformat() + "+01:00"
                end_datetime = full_endtime.isoformat() + "+01:00"
                
                event = {
                    "summary":summary,
                    "start":{"dateTime":start_datetime, "date":None},
                    "end":{"dateTime":end_datetime, "date":None}
                }

            except HttpError as error:
                print(f"An error occurred: {error}")
                
                
            event = service.events().insert(calendarId='primary', body=event).execute()
            print(f'Event created : {event.get("htmlLink")}')
            
            # Redirect to confirmation page after creating calendar event.
            return redirect(reverse('appointment-confirm', args=[str(appointment.id)]))
        
    else:
        form = CalendarModelForm()
        
    context = {'form':form}
    return render(request, 'appointment_form.html', context)

@login_required
def confirm_appointment(request, pk):
    """This view returns the appointment details confirmation page to the patient"""

    appointment = get_object_or_404(Calendar, id=pk)
    context = {'appointment':appointment}
    return render(request, 'confirmation.html', context)
    
            
