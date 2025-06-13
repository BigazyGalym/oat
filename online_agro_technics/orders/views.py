from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order, ServiceType
from accounts.models import Profile
from django import forms

# Форма класы
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['service_type', 'address', 'cost', 'district', 'phone_number']
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # Таңдау тізімдері
    service_type = forms.ModelChoiceField(queryset=ServiceType.objects.all(), empty_label="Таңдаңыз", label="Қызмет түрі")
    district = forms.ChoiceField(choices=Profile.DISTRICT_CHOICES, label="Район")

@login_required
def worker_orders(request):
    try:
        profile = request.user.profile
        if not profile.is_worker or not profile.district or not profile.service_type:
            messages.error(request, 'Заполните район и тип услуги в профиле.')
            return redirect('accounts:edit_profile')

        active_order = Order.objects.filter(worker_id=request.user, status__in=['accepted', 'in_progress']).first()
        if active_order:
            messages.info(request, f'У вас уже есть активный заказ: {active_order.id}')
            return render(request, 'worker/orders.html', {'available_orders': [], 'active_order': active_order})

        available_orders = Order.objects.filter(
            status='available',
            district=profile.district,
            service_type=profile.service_type
        )
        return render(request, 'worker/orders.html', {'available_orders': available_orders})
    except Profile.DoesNotExist:
        messages.error(request, 'Создайте профиль.')
        return redirect('accounts:create_profile')

@login_required
def worker_dashboard(request):
    try:
        profile = request.user.profile
        if profile.role != 'worker':
            messages.error(request, 'У вас нет прав доступа к этой странице.')
            return redirect('home')

        # Текущий заказ (принятый или в процессе)
        current_order = Order.objects.filter(worker_id=request.user, status__in=['accepted', 'in_progress']).first()

        # Доступные заказы
        available_orders = Order.objects.filter(status='available').exclude(worker_id=request.user)

        # Завершенные заказы
        completed_orders = Order.objects.filter(worker_id=request.user, status='completed')

        # Статистика заказов
        order_stats = {
            'available': Order.objects.filter(status='available').count(),
            'accepted': Order.objects.filter(status='accepted').count(),
            'in_progress': Order.objects.filter(status='in_progress').count(),
            'completed': Order.objects.filter(status='completed').count(),
        }

        context = {
            'profile': profile,
            'current_order': current_order,
            'available_orders': available_orders,
            'completed_orders': completed_orders,
            'order_stats': order_stats,
        }
        return render(request, 'worker/dashboard.html', context)
    except Exception as e:
        messages.error(request, f'Произошла ошибка: {str(e)}')
        return redirect('home')

@login_required
def accept_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, status='available')
        if request.method == 'POST':
            order.worker_id = request.user
            order.status = 'accepted'
            order.save()
            messages.success(request, 'Заказ успешно принят.')
            return redirect('orders:worker_dashboard')
        return render(request, 'worker/dashboard.html', {'order': order})
    except Order.DoesNotExist:
        messages.error(request, 'Заказ не найден или уже принят.')
        return redirect('orders:worker_dashboard')

@login_required
def start_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, status='accepted', worker_id=request.user)
        if request.method == 'POST':
            order.status = 'in_progress'
            order.save()
            messages.success(request, 'Работа начата.')
            return redirect('orders:worker_dashboard')
        return render(request, 'worker/dashboard.html', {'order': order})
    except Order.DoesNotExist:
        messages.error(request, 'Заказ не найден или не принят вами.')
        return redirect('orders:worker_dashboard')
    
    
@login_required
def complete_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, worker_id=request.user, status='in_progress')
        order.status = 'completed'
        order.save()
        profile = request.user.profile
        profile.completed_orders += 1
        profile.save()
        messages.success(request, 'Заказ завершен.')
        return redirect('orders:worker_dashboard')
    except Order.DoesNotExist:
        messages.error(request, 'Заказ не найден.')
        return redirect('orders:worker_orders')

@login_required
def rate_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, customer_id=request.user, status='completed')
        if request.method == 'POST':
            rating = int(request.POST.get('rating'))
            order.rating = rating
            order.save()
            worker_profile = order.worker_id.profile
            worker_profile.rating = (worker_profile.rating * worker_profile.completed_orders + rating) / (worker_profile.completed_orders + 1)
            worker_profile.save()
            messages.success(request, 'Оценка добавлена.')
            return redirect('orders:customer_dashboard')
        return render(request, 'customer/rate_order.html', {'order': order})
    except Order.DoesNotExist:
        messages.error(request, 'Заказ не найден.')
        return redirect('orders:customer_dashboard')

@login_required
def customer_dashboard(request):
    orders = Order.objects.filter(customer_id=request.user)
    profile = request.user.profile
    return render(request, 'customer/dashboard.html', {
        'orders': orders,
        'profile': profile,
    })

@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.customer_id = request.user
            order.status = 'available'
            order.save()
            messages.success(request, f'Заказ успешно создан! Номер заказа: {order.id}')
            return redirect('orders:customer_dashboard')
    else:
        form = OrderForm(initial={'address': 'Almaty', 'rating': 5})
    return render(request, 'orders/create_order.html', {'form': form})


@login_required
def cancel_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, worker_id=request.user, status__in=['accepted', 'in_progress'])
        if request.method == 'POST':
            order.worker_id = None
            order.status = 'available'
            order.save()
            messages.success(request, 'Заказ успешно отменен.')
            return redirect('orders:worker_orders')
        return render(request, 'worker/orders.html', {'active_order': order})
    except Order.DoesNotExist:
        messages.error(request, 'Заказ не найден или вам не принадлежит.')
        return redirect('orders:worker_orders')
    

@login_required
def cancel_customer_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id, customer_id=request.user, status='available')
        if request.method == 'POST':
            order.delete()
            messages.success(request, 'Заказ успешно отменен.')
            return redirect('orders:customer_dashboard')
        return render(request, 'customer/dashboard.html', {'order': order})
    except Order.DoesNotExist:
        messages.error(request, 'Заказ не найден или вам не принадлежит.')
        return redirect('orders:customer_dashboard')