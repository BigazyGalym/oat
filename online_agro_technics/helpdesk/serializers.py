from rest_framework import serializers
from .models import Ticket, TicketResponse

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'title', 'description', 'service_type', 'status', 'priority', 'created_at', 'updated_at', 'file']

class TicketResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketResponse
        fields = ['id', 'ticket', 'message', 'created_at', 'file']