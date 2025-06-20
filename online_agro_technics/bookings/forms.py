from django import forms
from .models import Booking, WorkerAvailability
from orders.models import ServiceType

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service_type', 'notes']
        labels = {
            'service_type': 'Қызмет түрі',
            'notes': 'Ескертпелер',
        }
        widgets = {
            'notes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Қосымша ақпарат енгізіңіз'}),
        }

    service_type = forms.ModelChoiceField(
        queryset=ServiceType.objects.all(),
        empty_label="Қызмет түрін таңдаңыз",
        label="Қызмет түрі"
    )

class WorkerAvailabilityForm(forms.ModelForm):
    class Meta:
        model = WorkerAvailability
        fields = ['service_type', 'start_time', 'end_time']
        labels = {
            'service_type': 'Қызмет түрі',
            'start_time': 'Басталу уақыты',
            'end_time': 'Аяқталу уақыты',
        }
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    service_type = forms.ModelChoiceField(
        queryset=ServiceType.objects.all(),
        empty_label="Қызмет түрін таңдаңыз",
        label="Қызмет түрі"
    )