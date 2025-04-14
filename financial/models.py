from django.db import models

class ExpenseRevenue(models.Model):
    TYPE_CHOICES = (
        ('expense', 'صادر'),
        ('revenue', 'وارد'),
    )
    record_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    date = models.DateField()
    # Optional link to a purchase (auto-created revenues only)
    purchase = models.OneToOneField(
        'customers.Purchase',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='financial_record'
    )

    def __str__(self):
        return f"{self.record_type.capitalize()} - {self.amount} on {self.date}"
