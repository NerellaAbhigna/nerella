from django.db import models
from django.contrib.auth.models import User
import random

def generate_unique_barcode():
    while True:
        barcode = str(random.randint(1000000000, 9999999999))  # 10-digit number
        if not Product.objects.filter(barcode=barcode).exists():
            return barcode

class Product(models.Model):
    name = models.CharField(max_length=200)
    sub_type = models.CharField(max_length=100, default="Unknown")
    color = models.CharField(max_length=50, default="Unknown")
    category = models.CharField(max_length=100, default="General")
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True, blank=True)
    barcode = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = f"SKU{random.randint(100000, 999999)}"
        if not self.barcode:
            self.barcode = generate_unique_barcode()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Invoice(models.Model):
    customer_name = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} - {self.customer_name}"


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    color = models.CharField(max_length=50, default="Unknown")

    def save(self, *args, **kwargs):
        if not self.pk:  # Deduct stock only on creation
            self.product.stock -= self.quantity
            self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
