from django import forms
from customers.models import Customer
from .models import Purchase, PurchaseItem
from inventory.models import InventoryItem
from django.forms import modelformset_factory

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['customer']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Sort by newest customer first
        self.fields['customer'].queryset = Customer.objects.order_by('-id')

class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['inventory_item', 'quantity', 'unit_price']
        widgets = {
            'quantity': forms.NumberInput(attrs={'min': 1, 'class': 'form-control quantity'}),
            'unit_price': forms.NumberInput(attrs={'step': 0.01, 'class': 'form-control unit-price'}),
        }

PurchaseItemFormSet = modelformset_factory(
    PurchaseItem,
    form=PurchaseItemForm,
    extra=1,
    can_delete=True
)
