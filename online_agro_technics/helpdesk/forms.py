from django import forms
from .models import Ticket, TicketResponse
from orders.models import ServiceType

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'service_type', 'priority', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Тікет тақырыбын енгізіңіз'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Мәселені сипаттаңыз'}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'title': 'Тақырып',
            'description': 'Сипаттама',
            'service_type': 'Қызмет түрі',
            'priority': 'Басымдық',
            'file': 'Файл',
        }

    service_type = forms.ModelChoiceField(
        queryset=ServiceType.objects.all(),
        empty_label="Қызмет түрін таңдаңыз",
        required=False,
        label="Қызмет түрі"
    )

class TicketResponseForm(forms.ModelForm):
    class Meta:
        model = TicketResponse
        fields = ['message', 'file']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Жауабыңызды жазыңыз'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'message': 'Хабарлама',
            'file': 'Файл',
        }