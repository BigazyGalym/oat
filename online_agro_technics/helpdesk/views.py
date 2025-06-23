from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Ticket, TicketResponse
from .forms import TicketForm, TicketResponseForm
from accounts.models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import TicketSerializer, TicketResponseSerializer

def is_admin(user):
    return user.profile.is_admin


@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.status = 'open'
            ticket.save()
            messages.success(request, 'Тикет успешно создан.')
            return redirect('helpdesk:ticket_list')
    else:
        form = TicketForm()
    return render(request, 'helpdesk/create_ticket.html', {'form': form})


@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = TicketResponseForm(request.POST, request.FILES)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.ticket = ticket
            response.save()
            ticket.status = 'in_progress'
            ticket.save()
            messages.success(request, 'Ответ добавлен.')
            return redirect('helpdesk:ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketResponseForm()
    return render(request, 'helpdesk/ticket_detail.html', {'ticket': ticket, 'form': form})


@login_required
@user_passes_test(is_admin, login_url='/accounts/login/')
def ticket_close(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    ticket.status = 'closed'
    ticket.save()
    messages.success(request, 'Тикет закрыт.')
    return redirect('helpdesk:ticket_detail', ticket_id=ticket.id)


@login_required
def user_ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user != ticket.user and not request.user.profile.is_admin:
        messages.error(request, 'У вас нет доступа к этому тикету.')
        return redirect('helpdesk:ticket_list')
    if request.method == 'POST':
        form = TicketResponseForm(request.POST, request.FILES)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.ticket = ticket
            response.save()
            ticket.status = 'in_progress'
            ticket.save()
            messages.success(request, 'Ответ добавлен.')
            return redirect('helpdesk:user_ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketResponseForm()
    return render(request, 'helpdesk/user_ticket_detail.html', {'ticket': ticket, 'form': form})


@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'helpdesk/ticket_list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if ticket.user != request.user and not request.user.profile.is_admin():
        messages.error(request, 'Сізге бұл тікетті қарауға рұқсат жоқ.')
        return redirect('helpdesk:ticket_list')
    if request.method == 'POST':
        form = TicketResponseForm(request.POST, request.FILES)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.ticket = ticket
            response.save()
            # Статусты өзгерту (оператор жауап берсе)
            if request.user.profile.is_admin() or request.user.profile.is_worker:
                ticket.status = 'in_progress'
                ticket.save()
            messages.success(request, 'Жауап қосылды.')
            return redirect('helpdesk:ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketResponseForm()
    return render(request, 'helpdesk/ticket_detail.html', {'ticket': ticket, 'form': form})

@login_required
def ticket_close(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user.profile.is_admin() or request.user.profile.is_worker:
        ticket.status = 'closed'
        ticket.save()
        messages.success(request, 'Тікет жабылды.')
    else:
        messages.error(request, 'Сізге тікетті жабуға рұқсат жоқ.')
    return redirect('helpdesk:ticket_detail', ticket_id=ticket.id)

# API көріністері (Dialogflow үшін)
class TicketCreateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TicketListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)