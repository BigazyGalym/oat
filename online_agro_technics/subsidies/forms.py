from django import forms
from .models import SubsidyInquiry

class SubsidyInquiryForm(forms.ModelForm):
    class Meta:
        model = SubsidyInquiry
        fields = ['message']
        labels = {
            'message': 'Сұрау',
        }
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Субсидия туралы сұрағыңызды жазыңыз'}),
        }