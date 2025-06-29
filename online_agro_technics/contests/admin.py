from django.contrib import admin
from .models import Contest, ContestEntry

@admin.register(Contest)
class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'start_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'start_date'
    list_per_page = 20
    list_editable = ('is_active',)

@admin.register(ContestEntry)
class ContestEntryAdmin(admin.ModelAdmin):
    list_display = ('contest', 'user', 'created_at')
    list_filter = ('contest',)
    search_fields = ('user__username', 'submission')
    list_per_page = 20