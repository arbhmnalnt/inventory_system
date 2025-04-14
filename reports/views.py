from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from inventory.models import InventoryItem
from customers.models import Customer, Purchase
from financial.models import ExpenseRevenue
from django.db.models import Sum
from datetime import date

@login_required
def reports_index(request):
    return render(request, 'reports/index.html')

@login_required
def inventory_summary(request):
    items = InventoryItem.objects.all()
    return render(request, 'reports/inventory_summary.html', {'items': items})

@login_required
def purchase_summary(request):
    purchases = Purchase.objects.select_related('customer').prefetch_related('items__inventory_item').order_by('-purchase_date')

    return render(request, 'reports/purchase_summary.html', {'purchases': purchases})

@login_required
def financial_summary(request):
    records = ExpenseRevenue.objects.all()
    total_expense = records.filter(record_type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    total_revenue = records.filter(record_type='revenue').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_revenue - total_expense
    return render(request, 'reports/financial_summary.html', {
        'records': records,
        'total_expense': total_expense,
        'total_revenue': total_revenue,
        'balance': balance,
    })
