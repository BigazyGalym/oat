from django import forms
from .models import Contest, ContestEntry

class ContestForm(forms.ModelForm):
    class Meta:
        model = Contest
        fields = ['title', 'description', 'start_date', 'end_date', 'prize']
        labels = {
            'title': 'Тақырып',
            'description': 'Сипаттама',
            'start_date': 'Басталу уақыты',
            'end_date': 'Аяқталу уақыты',
            'prize': 'Сыйлық',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Конкурс тақырыбын енгізіңіз'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Конкурс сипаттамасын енгізіңіз'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'prize': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Сыйлықты сипаттаңыз'}),
        }

class ContestEntryForm(forms.ModelForm):
    class Meta:
        model = ContestEntry
        fields = ['submission']
        labels = {
            'submission': 'Жұмыс',
        }
        widgets = {
            'submission': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Конкурсқа қатысу үшін жұмысыңызды сипаттаңыз'}),
        }