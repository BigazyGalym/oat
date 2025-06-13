from django import forms
from django.contrib.auth import get_user_model
from django.db import transaction
from orders.models import ServiceType
from .models import Profile


CustomUser = get_user_model()

class CustomAuthenticationForm(forms.Form):
    username = forms.EmailField(label="Email", max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Введите email'})

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('username')
        if email:
            try:
                user = self.user_cache = CustomUser.objects.get(email=email)
                if not user:
                    raise forms.ValidationError("Пользователь с таким email не найден.")
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Пользователь с таким email не найден.")
        return cleaned_data

class SignUpForm(forms.ModelForm):
    role = forms.ChoiceField(choices=[('customer', 'Заказчик'), ('worker', 'Рабочий'), ('admin', 'Админ')], label='Роль')
    description = forms.CharField(widget=forms.Textarea, required=False, label='Описание')
    avatar = forms.ImageField(required=False, label='Аватар')
    service_type = forms.ModelChoiceField(
        queryset=ServiceType.objects.all(),
        required=False,
        label='Тип услуги',
        empty_label='Выберите тип услуги'
    )
    district = forms.ChoiceField(
        choices=[('', 'Выберите район')] + [
            ('almalinsky', 'Алмалинский район'),
            ('alatau', 'Алатауский район'),
            ('auezov', 'Ауэзовский район'),
            ('bostandyk', 'Бостандыкский район'),
            ('zhetysu', 'Жетысуский район'),
            ('medeu', 'Медеуский район'),
            ('nauryzbay', 'Наурызбайский район'),
            ('turksib', 'Турксибский район'),
        ],
        required=False,
        label='Район'
    )
    phone_number = forms.CharField(max_length=15, label='Телефон', required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            with transaction.atomic():
                user.set_password(self.cleaned_data.get('password'))
                user.is_active = False
                user.save()
                from .models import Profile  # Кешіктірілген импорт
                profile = Profile.objects.create(
                    user=user,
                    role=self.cleaned_data['role'],
                    description=self.cleaned_data['description'],
                    avatar=self.cleaned_data['avatar'],
                    is_worker=(self.cleaned_data['role'] == 'worker'),
                    service_type=self.cleaned_data['service_type'] if self.cleaned_data['role'] == 'worker' else None,
                    district=self.cleaned_data['district'] if self.cleaned_data['role'] == 'worker' else None,
                    phone_number=self.cleaned_data['phone_number']
                )
        return user

class ProfileForm(forms.ModelForm):
    service_type = forms.ModelChoiceField(
        queryset=ServiceType.objects.all(),
        required=False,
        label='Тип услуги',
        empty_label='Выберите тип услуги'
    )
    district = forms.ChoiceField(
        choices=[('', 'Выберите район')] + [
            ('almalinsky', 'Алмалинский район'),
            ('alatau', 'Алатауский район'),
            ('auezov', 'Ауэзовский район'),
            ('bostandyk', 'Бостандыкский район'),
            ('zhetysu', 'Жетысуский район'),
            ('medeu', 'Медеуский район'),
            ('nauryzbay', 'Наурызбайский район'),
            ('turksib', 'Турксибский район'),
        ],
        required=False,
        label='Район'
    )
    phone_number = forms.CharField(max_length=15, label='Телефон', required=True)

    class Meta:
        model = Profile
        fields = ['role', 'description', 'avatar', 'service_type', 'district', 'phone_number']
        labels = {
            'role': 'Роль',
            'description': 'Описание',
            'avatar': 'Аватар',
            'phone_number': 'Телефон',
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.is_worker = (profile.role == 'worker')
            profile.save()
            if profile.service_type and not profile.is_worker:
                profile.service_type = None
            if not profile.is_worker and profile.role != 'admin':
                profile.district = None
            profile.save()
        return profile

class VerificationForm(forms.Form):
    email = forms.EmailField(label='Электронная почта')
    code = forms.CharField(max_length=6, label='Код подтверждения', widget=forms.TextInput(attrs={'placeholder': 'Введите 6-значный код'}))