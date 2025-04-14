from django.contrib import admin
from .models import ExpenseRevenue

@admin.register(ExpenseRevenue)
class ExpenseRevenueAdmin(admin.ModelAdmin):
    list_display = ('record_type', 'amount', 'date', 'purchase')
    list_filter = ('record_type', 'date')
    search_fields = ('description',)
