from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, EmailVerificationCode
from orders.models import ServiceType
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Введите email'})

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')
        if email:
            try:
                user = self.user_cache = self.get_user(email)
                if not user:
                    raise forms.ValidationError("Пользователь с таким email не найден.")
            except self.UserModel.DoesNotExist:
                raise forms.ValidationError("Пользователь с таким email не найден.")
        return cleaned_data

CustomUser = get_user_model()

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, label='Роль')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Описание')
    avatar = forms.ImageField(required=False, label='Аватар')
    service_type = forms.ModelChoiceField(
        queryset=ServiceType.objects.all(),
        required=False,
        label='Тип услуги',
        empty_label='Выберите тип услуги'  # Это допустимо для ModelChoiceField
    )
    district = forms.ChoiceField(
        choices=[('', 'Выберите район')] + list(Profile.DISTRICT_CHOICES),  # Добавлен пустой вариант
        required=False,
        label='Район'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'role', 'description', 'avatar', 'service_type', 'district']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }
        error_messages = {
            'username': {'required': 'Введите имя пользователя'},
            'email': {'required': 'Введите email'},
            'password1': {'required': 'Введите пароль'},
            'password2': {'required': 'Подтвердите пароль'},
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['service_type'].queryset = ServiceType.objects.all()
        self.fields['district'].choices = [('', 'Выберите район')] + list(Profile.DISTRICT_CHOICES)

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            with transaction.atomic():
                user.is_active = False
                user.save()
                profile = Profile.objects.create(
                    user=user,
                    role=self.cleaned_data['role'],
                    description=self.cleaned_data['description'],
                    avatar=self.cleaned_data['avatar'],
                    is_worker=(self.cleaned_data['role'] == 'worker'),
                    service_type=self.cleaned_data['service_type'] if self.cleaned_data['role'] == 'worker' else None,
                    district=self.cleaned_data['district'] if self.cleaned_data['role'] == 'worker' else None
                )
        return user

class ProfileForm(forms.ModelForm):
    service_type = forms.ModelChoiceField(
        queryset=ServiceType.objects.all(),
        required=False,
        label='Тип услуги',
        empty_label='Выберите тип услуги'  # Это допустимо для ModelChoiceField
    )
    district = forms.ChoiceField(
        choices=[('', 'Выберите район')] + list(Profile.DISTRICT_CHOICES),  # Добавлен пустой вариант
        required=False,
        label='Район'
    )

    class Meta:
        model = Profile
        fields = ['role', 'description', 'avatar', 'service_type', 'district']
        labels = {
            'role': 'Роль',
            'description': 'Описание',
            'avatar': 'Аватар',
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.is_worker = (profile.role == 'worker')
            profile.save()
            if profile.service_type and not profile.is_worker:
                profile.service_type = None
            if not profile.is_worker and profile.role != 'admin':  # Admin-ға district міндетті емес
                profile.district = None
            profile.save()
        return profile

class VerificationForm(forms.Form):
    email = forms.EmailField(label='Электронная почта')
    code = forms.CharField(max_length=6, label='Код подтверждения', widget=forms.TextInput(attrs={'placeholder': 'Введите 6-значный код'}))