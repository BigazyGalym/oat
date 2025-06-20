from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Booking, WorkerAvailability
from .forms import BookingForm, WorkerAvailabilityForm
from accounts.models import Profile
from orders.models import ServiceType

@login_required
def worker_availability(request):
    if not request.user.profile.is_worker:
        messages.error(request, 'Тек жұмысшылар бос уақытты орната алады.')
        return redirect('accounts:dashboard')
    if request.method == 'POST':
        form = WorkerAvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.worker = request.user
            if availability.start_time >= availability.end_time:
                messages.error(request, 'Аяқталу уақыты басталу уақытынан кейін болуы керек.')
            elif availability.start_time < timezone.now():
                messages.error(request, 'Басталу уақыты болашақта болуы керек.')
            else:
                availability.save()
                messages.success(request, 'Бос уақыт қосылды.')
                return redirect('bookings:worker_availability')
    else:
        form = WorkerAvailabilityForm()
    availabilities = WorkerAvailability.objects.filter(worker=request.user, is_available=True, end_time__gt=timezone.now())
    return render(request, 'bookings/worker_availability.html', {'form': form, 'availabilities': availabilities})

@login_required
def create_booking(request, availability_id):
    availability = get_object_or_404(WorkerAvailability, id=availability_id, is_available=True)
    if request.user == availability.worker:
        messages.error(request, 'Өзіңіздің бос уақытыңызды брондай алмайсыз.')
        return redirect('bookings:available_workers')
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.worker = availability.worker
            booking.availability = availability
            booking.save()
            availability.is_available = False
            availability.save()
            messages.success(request, 'Бронь сәтті жасалды.')
            return redirect('bookings:customer_bookings')
    else:
        form = BookingForm(initial={'service_type': availability.service_type})
    return render(request, 'bookings/create_booking.html', {'form': form, 'availability': availability})

@login_required
def available_workers(request):
    service_type_id = request.GET.get('service_type')
    district = request.GET.get('district')
    availabilities = WorkerAvailability.objects.filter(is_available=True, end_time__gt=timezone.now())
    if service_type_id:
        availabilities = availabilities.filter(service_type_id=service_type_id)
    if district:
        availabilities = availabilities.filter(worker__profile__district=district)
    service_types = ServiceType.objects.all()
    districts = Profile.DISTRICT_CHOICES
    return render(request, 'bookings/available_workers.html', {
        'availabilities': availabilities,
        'service_types': service_types,
        'districts': districts,
        'selected_service_type': service_type_id,
        'selected_district': district,
    })

@login_required
def customer_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'bookings/customer_bookings.html', {'bookings': bookings})

@login_required
def worker_bookings(request):
    if not request.user.profile.is_worker:
        messages.error(request, 'Тек жұмысшылар броньдарды көре алады.')
        return redirect('accounts:dashboard')
    bookings = Booking.objects.filter(worker=request.user).order_by('-created_at')
    return render(request, 'bookings/worker_bookings.html', {'bookings': bookings})

@login_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, worker=request.user, status='pending')
    if request.method == 'POST':
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, 'Бронь расталды.')
        return redirect('bookings:worker_bookings')
    return render(request, 'bookings/confirm_booking.html', {'booking': booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if booking.customer != request.user and booking.worker != request.user:
        messages.error(request, 'Сіз бұл броньды жоя алмайсыз.')
        return redirect('bookings:customer_bookings')
    if request.method == 'POST':
        booking.availability.is_available = True
        booking.availability.save()
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, 'Бронь жойылды.')
        if request.user == booking.customer:
            return redirect('bookings:customer_bookings')
        return redirect('bookings:worker_bookings')
    return render(request, 'bookings/cancel_booking.html', {'booking': booking})