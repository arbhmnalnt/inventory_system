from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Purchase, PurchaseItem, Customer
from .forms import PurchaseForm, PurchaseItemFormSet
from inventory.models import InventoryItem
from financial.models import ExpenseRevenue
from datetime import date
from django.forms import modelformset_factory
from django.http import JsonResponse
from django.db.models import Q



# ---------------------
# PURCHASE CRUD VIEWS
# ---------------------

@login_required
def get_item_price(request):
    item_id = request.GET.get('item_id')
    try:
        item = InventoryItem.objects.get(pk=item_id)
        return JsonResponse({'price': str(item.price)})
    except InventoryItem.DoesNotExist:
        return JsonResponse({'price': 0})


@login_required
def purchase_list(request):
    purchases = Purchase.objects.all().order_by('-purchase_date')
    return render(request, 'customers/purchase_list.html', {'purchases': purchases})

@login_required
def purchase_detail(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    return render(request, 'customers/purchase_detail.html', {'purchase': purchase})

@login_required
def purchase_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        formset = PurchaseItemFormSet(request.POST, queryset=PurchaseItem.objects.none())
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                purchase = form.save(commit=False)
                purchase.created_by = request.user
                purchase.save()

                total = 0
                for item_form in formset:
                    if item_form.cleaned_data and not item_form.cleaned_data.get('DELETE'):
                        item = item_form.save(commit=False)
                        item.purchase = purchase
                        item.total_price = item.unit_price * item.quantity
                        item.save()

                        # reduce stock
                        item.inventory_item.quantity -= item.quantity
                        item.inventory_item.save()

                        total += item.total_price

                purchase.total_price = total
                purchase.save()

                # create one financial record
                ExpenseRevenue.objects.create(
                    record_type='revenue',
                    amount=total,
                    description=f"Purchase #{purchase.id} for {purchase.customer.name}",
                    date=date.today(),
                    purchase=purchase
                )
                messages.success(request, "عملية شراء مكتملة .")
                return redirect('purchase_list')
    else:
        form = PurchaseForm()
        formset = PurchaseItemFormSet(queryset=PurchaseItem.objects.none())

    return render(request, 'customers/purchase_form.html', {
        'form': form,
        'formset': formset
    })# ---------------------
# PURCHASE UPDATE
# ---------------------
@login_required
def purchase_update(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)
    existing_items = list(purchase.items.all())

    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        formset = PurchaseItemFormSet(request.POST, queryset=purchase.items.all())
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()

                # Revert inventory stock
                for item in existing_items:
                    if item.inventory_item:
                        item.inventory_item.quantity += item.quantity
                        item.inventory_item.save()

                total = 0
                new_items = formset.save(commit=False)

                # Delete any marked for deletion
                for del_form in formset.deleted_objects:
                    del_form.delete()

                # Save new/updated items
                for item in new_items:
                    item.purchase = purchase
                    item.total_price = item.unit_price * item.quantity
                    item.save()

                    # Decrease inventory again
                    item.inventory_item.quantity -= item.quantity
                    item.inventory_item.save()

                    total += item.total_price

                purchase.total_price = total
                purchase.save()

                # Update linked revenue
                try:
                    rev = purchase.financial_record
                    rev.amount = total
                    rev.description = f"Updated purchase #{purchase.id} for {purchase.customer.name}"
                    rev.save()
                except ExpenseRevenue.DoesNotExist:
                    ExpenseRevenue.objects.create(
                        record_type='revenue',
                        amount=total,
                        description=f"Purchase #{purchase.id} for {purchase.customer.name}",
                        date=purchase.purchase_date,
                        purchase=purchase
                    )

                messages.success(request, "تم تسجيل عملية بيع جديدة بنجاح.")
                return redirect('purchase_list')
    else:
        form = PurchaseForm(instance=purchase)
        formset = PurchaseItemFormSet(queryset=purchase.items.all())

    return render(request, 'customers/purchase_form.html', {
        'form': form,
        'formset': formset,
        'update': True,
        'purchase': purchase
    })

# ---------------------
# PURCHASE DELETE
# ---------------------

@login_required
def purchase_delete(request, pk):
    purchase = get_object_or_404(Purchase, pk=pk)

    if request.method == 'POST':
        with transaction.atomic():
            # Restore inventory quantities
            for item in purchase.items.all():
                if item.inventory_item:
                    item.inventory_item.quantity += item.quantity
                    item.inventory_item.save()

            # Delete related financial record
            try:
                purchase.financial_record.delete()
            except:
                pass

            # Delete the purchase and its items (via cascade)
            purchase.delete()

            messages.success(request, "تم حذف عملية الشراء والإضافة للمخزون وحذف سجل الدفع المرتبط.")
            return redirect('purchase_list')

    return render(request, 'customers/purchase_confirm_delete.html', {'purchase': purchase})

# ---------------------
# OPTIONAL: CUSTOMER CRUD VIEWS
# (These are provided for context if you need them.)
@login_required
def customer_list(request):
    query = request.GET.get('q')
    customers = Customer.objects.all()
    if query:
        customers = customers.filter(
            Q(name__icontains=query) |
            Q(email__icontains=query) |
            Q(phone__icontains=query)
        )
    return render(request, 'customers/customer_list.html', {'customers': customers})

@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    # Retrieves purchase history using the related_name='purchases'
    purchases = customer.purchases.all()
    return render(request, 'customers/customer_detail.html', {'customer': customer, 'purchases': purchases})

@login_required
def customer_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        Customer.objects.create(name=name, email=email, phone=phone, address=address)
        return redirect('customer_list')
    return render(request, 'customers/customer_form.html')

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.name = request.POST.get('name')
        customer.email = request.POST.get('email')
        customer.phone = request.POST.get('phone')
        customer.address = request.POST.get('address')
        customer.save()
        return redirect('customer_list')
    return render(request, 'customers/customer_form.html', {'customer': customer})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})
