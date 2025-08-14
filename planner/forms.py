from django import forms
from planner.models import Booking
from django.core.exceptions import ValidationError
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'start_date', 'end_date']  # Matching your model
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
        }
        labels = {
            'service': 'Choose Service',
            'start_date': 'Pick-up/Check-in Date',
            'end_date': 'Drop-off/Check-out Date',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date < timezone.now():
                raise ValidationError("Start date cannot be in the past")
            if end_date <= start_date:
                raise ValidationError("End date must be after start date")
        
        return cleaned_data
