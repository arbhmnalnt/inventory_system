from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import ExpenseRevenue
from .forms import ExpenseRevenueForm

@login_required
def financial_list(request):
    records = ExpenseRevenue.objects.all().order_by('-date')
    total_expense = records.filter(record_type='expense').aggregate(total=models.Sum('amount'))['total'] or 0
    total_revenue = records.filter(record_type='revenue').aggregate(total=models.Sum('amount'))['total'] or 0
    balance = total_revenue - total_expense
    return render(request, 'financial/financial_list.html', {
        'records': records,
        'total_expense': total_expense,
        'total_revenue': total_revenue,
        'balance': balance,
    })

@login_required
def financial_create(request):
    if request.method == 'POST':
        form = ExpenseRevenueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Financial record added successfully.")
            return redirect('financial_list')
    else:
        form = ExpenseRevenueForm()
    return render(request, 'financial/financial_form.html', {'form': form})

@login_required
def financial_update(request, pk):
    record = get_object_or_404(ExpenseRevenue, pk=pk)
    if record.purchase:
        messages.warning(request, "You cannot edit a revenue record linked to a purchase.")
        return redirect('financial_list')

    if request.method == 'POST':
        form = ExpenseRevenueForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Financial record updated successfully.")
            return redirect('financial_list')
    else:
        form = ExpenseRevenueForm(instance=record)
    return render(request, 'financial/financial_form.html', {'form': form})

@login_required
def financial_delete(request, pk):
    record = get_object_or_404(ExpenseRevenue, pk=pk)
    if record.purchase:
        messages.warning(request, "You cannot delete a revenue record linked to a purchase.")
        return redirect('financial_list')

    if request.method == 'POST':
        record.delete()
        messages.success(request, "Financial record deleted successfully.")
        return redirect('financial_list')
    return render(request, 'financial/financial_confirm_delete.html', {'record': record})
