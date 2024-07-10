from django.urls import path
from .views import create_appointment, confirm_appointment


urlpatterns = [
    path('appointment-create-new/<int:pk>/', create_appointment, name='appointment-create'),
    path('appointment-confirm/<int:pk>/', confirm_appointment, name='appointment-confirm'),
]