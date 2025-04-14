from django import forms
from .models import ExpenseRevenue

class ExpenseRevenueForm(forms.ModelForm):
    class Meta:
        model = ExpenseRevenue
        fields = ['record_type', 'amount', 'description', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }
