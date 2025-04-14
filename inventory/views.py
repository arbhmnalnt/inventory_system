from django.shortcuts import render, get_object_or_404, redirect
from .models import InventoryItem, InventoryTransaction
from .forms import InventoryItemForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q





# Inventory Items CRUD
@login_required
def inventory_item_list(request):
    query = request.GET.get('q')
    items = InventoryItem.objects.all()
    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query)
        )
    return render(request, 'inventory/inventory_item_list.html', {'items': items, 'query': query})

@login_required
def inventory_item_create(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item added successfully.')
            return redirect('inventory_item_list')
    else:
        form = InventoryItemForm()
    return render(request, 'inventory/inventory_item_form.html', {'form': form})

def inventory_item_update(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully.')
            return redirect('inventory_item_list')
    else:
        form = InventoryItemForm(instance=item)
    return render(request, 'inventory/inventory_item_form.html', {'form': form})
@login_required
def inventory_item_delete(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('inventory_item_list')
    return render(request, 'inventory/inventory_item_delete_confirm.html', {'item': item})

# Inventory Transactions CRUD

@login_required
def inventory_transaction_list(request):
    transactions = InventoryTransaction.objects.all()
    return render(request, 'inventory/inventory_transaction_list.html', {'transactions': transactions})

@login_required
def inventory_transaction_create(request):
    items = InventoryItem.objects.all()
    if request.method == 'POST':
        item_id = request.POST.get('inventory_item')
        transaction_type = request.POST.get('transaction_type')
        quantity = request.POST.get('quantity')
        item = get_object_or_404(InventoryItem, pk=item_id)
        InventoryTransaction.objects.create(
            inventory_item=item,
            transaction_type=transaction_type,
            quantity=quantity
        )
        # Optionally adjust inventory quantity here based on type.
        return redirect('inventory_transaction_list')
    return render(request, 'inventory/inventory_transaction_form.html', {'items': items})
