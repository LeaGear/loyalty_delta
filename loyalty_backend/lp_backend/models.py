from django.db import models

# Create your models here.

class OperationType(models.TextChoices):
    PURCHASE = 'PURCHASE'
    REFUND = 'REFUND'
    BONUS = 'BONUS'


class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='Client Name')
    phone_number = models.CharField(unique=True, max_length=20, verbose_name='Client Phone Number')
    telegram_id = models.BigIntegerField(unique=True, verbose_name='Client Telegram ID')
    total_spent = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name='Total Spent')
    last_operation_date = models.DateField(null=True, blank=True, verbose_name='Last Operation Date')
    registered_at = models.DateField(auto_now_add=True, verbose_name='Registered Date')
    custom_discount = models.PositiveIntegerField(default=0, verbose_name='Custom Discount')

    def __str__(self):
        return f"{self.name} spent -> {self.total_spent} | Custom Discount -> {self.custom_discount}"


class Operation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, verbose_name='Operation for -> ')
    operation_type = models.CharField(max_length=20, choices=OperationType.choices, default=OperationType.PURCHASE, verbose_name='Operation Type')
    amount = models.DecimalField(default=0, max_digits=7, decimal_places=2, verbose_name='Operation Amount')
    operation_date = models.DateField(auto_now_add=True, verbose_name='Operation Date')

    def __str__(self):
        return f"{self.client} -> {self.operation_type} -> {self.amount} -> {self.operation_date}"

class DiscountTier(models.Model):
    name = models.CharField(max_length=30, verbose_name='Discount Tier Name')
    min_total = models.DecimalField(default=0, max_digits=8, decimal_places=2, unique=True, verbose_name='Minimum Discount Total')
    discount_percent = models.PositiveIntegerField(default=0, verbose_name='Discount Percentage')

    class Meta:
        ordering = ['-min_total']

    def __str__(self):
        return f"{self.name} | Spent -> {self.min_total} | Discount -> {self.discount_percent}%"