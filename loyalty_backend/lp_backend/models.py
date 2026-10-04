from django.db import models
from django.db.models.functions import Now


# Create your models here.

class OperationType(models.TextChoices):
    PURCHASE = 'PURCHASE'
    REFUND = 'REFUND'
    BONUS = 'BONUS'

class Client(models.Model):
    name = models.CharField(max_length=100, verbose_name='Client Name')
    phone_number = models.CharField(max_length=20, verbose_name='Client Phone Number')
    telegram_id = models.BigIntegerField(verbose_name='Client Telegram ID')
    total_spent = models.IntegerField(default=0, verbose_name='Total Spent')
    last_operation_date = models.DateField(null=True, blank=True, verbose_name='Last Operation Date')
    registered_at = models.DateField(auto_now_add=True, verbose_name='Registered Date')
    custom_discount = models.FloatField(default=0.0, verbose_name='Custom Discount')
    discount_value = models.FloatField(default=0.0, verbose_name='Discount Value')

    def __str__(self):
        return f"{self.name} spent - {self.total_spent} Discount - {self.discount_value}."

    def calculate_total_spent(self):
        self.discount_value = self.custom_discount + get_actual_discount_value(self.total_spent) #Need function
        self.save()

class Operation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Operation for -> ')
    operation_type = models.CharField(max_length=20, choices=OperationType.choices, default=OperationType.PURCHASE, verbose_name='Operation Type')
    amount = models.FloatField(default=0.0, verbose_name='Operation Amount')
    operation_date = models.DateField(auto_now_add=True, verbose_name='Operation Date')

    def __str__(self):
        return f"{self.client} -> {self.operation_type} -> {self.amount} -> {self.operation_date}"

    @property
    def calculate_operation_total(self, oper_type):
        pass