from django.contrib import admin
from .models import SubsidyInquiry

@admin.register(SubsidyInquiry)
class SubsidyInquiryAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'responded')
    list_filter = ('responded', 'created_at')
    search_fields = ('user__username', 'message')
    list_per_page = 20
    list_editable = ('responded',)