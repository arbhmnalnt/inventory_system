from django.db import models

class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # 💰 NEW
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class InventoryTransaction(models.Model):
    TRANSACTION_CHOICES = (
        ('import', 'Import'),
        ('export', 'Export'),
    )
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES)
    quantity = models.IntegerField()
    transaction_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.inventory_item.name} ({self.quantity})"
