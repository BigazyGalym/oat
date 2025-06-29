from django import forms
from .models import News

class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'image']
        labels = {
            'title': 'Тақырып',
            'content': 'Мазмұны',
            'image': 'Сурет',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Жаңалық тақырыбын енгізіңіз'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Жаңалық мәтінін енгізіңіз'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }