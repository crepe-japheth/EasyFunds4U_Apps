from django.contrib import admin
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'client_type', 'branch', 'status', 'created_at')
    search_fields = ('first_name', 'last_name', 'national_id', 'phone_number')
    list_filter = ('created_at', 'status', 'client_type', 'branch')
    ordering = ('-created_at',)