from django import forms
from .models import ForumPost, ForumComment

class ForumPostForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ['title', 'content']
        labels = {
            'title': 'Тақырып',
            'content': 'Мазмұны',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Жазба тақырыбын енгізіңіз'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Сипаттама немесе кеңес енгізіңіз'}),
        }

class ForumCommentForm(forms.ModelForm):
    class Meta:
        model = ForumComment
        fields = ['content']
        labels = {
            'content': 'Пікір',
        }
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Пікіріңізді жазыңыз'}),
        }