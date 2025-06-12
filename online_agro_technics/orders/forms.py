from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['service_type', 'description', 'longitude', 'latitude', 'address', 'cost', 'desired_time', 'district']
        labels = {
            'service_type': 'Тип услуги',
            'description': 'Описание',
            'longitude': 'Долгота',
            'latitude': 'Широта',
            'address': 'Адрес',
            'cost': 'Стоимость',
            'desired_time': 'Желаемое время выполнения',
            'district': 'Район',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['district'] = forms.ChoiceField(
            choices=[('', 'Выберите район')] + list(Order.DISTRICT_CHOICES),
            required=False,
            label='Район'
        )