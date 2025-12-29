from django.contrib import admin
from .models import Branch

@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'manager', 'created_at')
    search_fields = ('name', 'location', 'manager__username')
    list_filter = ('created_at',)
    ordering = ('name',)