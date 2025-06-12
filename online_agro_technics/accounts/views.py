import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
import threading
from django.utils import timezone
from .forms import SignUpForm, ProfileForm, VerificationForm
from .models import Profile, EmailVerificationCode, CustomUser
from orders.models import Order
from .forms import CustomAuthenticationForm  # Жаңа форма

# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomAuthenticationForm

def custom_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Вы успешно вошли.')
                next_url = request.GET.get('next', None)
                if next_url:
                    return redirect(next_url)
                # Рөлге байланысты бағыттау
                if hasattr(user, 'profile') and user.profile.role == 'customer':
                    return redirect('orders:customer_dashboard')
                elif hasattr(user, 'profile') and user.profile.role == 'worker':
                    return redirect('orders:worker_orders')
                else:
                    return redirect('home')  # Әдепкі бет
            else:
                messages.error(request, 'Неверный email или пароль.')
        else:
            messages.error(request, 'Проверьте введенные данные.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


logger = logging.getLogger('django')

def send_verification_code(user, code):
    subject = 'Код подтверждения для Agro Technics'
    message = f'Привет {user.username}!\nВаш код подтверждения: {code}\n\nВведите его на странице подтверждения в течение 10 минут.'
    from_email = 'galymbigazy@gmail.com'
    recipient_list = [user.email]
    try:
        result = send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        logger.info(f"Хат жіберілді: {result} - {user.email}")
    except Exception as e:
        logger.error(f"Хат жіберу қатесі: {str(e)}")

class EmailThread(threading.Thread):
    def __init__(self, user, code):
        self.user = user
        self.code = code
        threading.Thread.__init__(self)

    def run(self):
        send_verification_code(self.user, self.code)

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            code = get_random_string(length=6, allowed_chars='1234567890')
            expires_at = timezone.now() + timezone.timedelta(minutes=10)
            EmailVerificationCode.objects.create(user=user, code=code, expires_at=expires_at)
            EmailThread(user, code).start()
            messages.success(request, 'Регистрация успешна! Проверьте email.')
            return redirect('accounts:verify_code')  # Use namespaced URL
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user and user.is_active:
            login(request, user)
            return redirect('accounts:dashboard')  # Use namespaced URL
        messages.error(request, 'Неверные данные или аккаунт не активирован.')
    return render(request, 'accounts/login.html')

def verify_code(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            code = form.cleaned_data['code']
            try:
                user = CustomUser.objects.get(email=email)
                verification = EmailVerificationCode.objects.filter(user=user, code=code).first()
                if verification and not verification.is_expired():
                    user.is_active = True
                    user.save()
                    verification.delete()
                    login(request, user)
                    messages.success(request, 'Аккаунт активирован!')
                    return redirect('accounts:dashboard')
                messages.error(request, 'Неверный код или срок истёк.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Пользователь не найден.')
    else:
        form = VerificationForm()
    return render(request, 'accounts/verify_email.html', {'form': form})

@login_required
def dashboard(request):
    try:
        profile = request.user.profile
        if profile.role == 'worker':
            return redirect('orders:worker_orders')
        elif profile.role == 'admin':
            return redirect('accounts:admin_dashboard')
        return redirect('orders:customer_dashboard')
    except Profile.DoesNotExist:
        messages.error(request, 'Создайте профиль.')
        return redirect('accounts:create_profile')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён.')
            return redirect('accounts:dashboard')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'accounts/edit_profile.html', {'form': form})

@login_required
def create_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Профиль создан.')
            return redirect('accounts:dashboard')
    else:
        form = ProfileForm()
    return render(request, 'accounts/create_profile.html', {'form': form})

@login_required
def admin_dashboard(request):
    if not request.user.profile.is_admin():
        messages.error(request, 'У вас нет прав доступа.')
        return redirect('accounts:dashboard')
    orders = Order.objects.all()
    return render(request, 'accounts/admin_dashboard.html', {'orders': orders})

def custom_logout(request):
    request.session.flush()
    logout(request)
    response = HttpResponseRedirect(reverse('accounts:login'))
    response.delete_cookie('sessionid')
    return response