from django.contrib import admin
from .models import Product, Invoice, InvoiceItem

# ---------------- Product Admin ----------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_type', 'color', 'category', 'price', 'stock', 'sku', 'barcode')
    list_filter = ('category', 'sub_type', 'color')
    search_fields = ('name', 'sku', 'barcode')

# ---------------- Invoice Admin ----------------
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'total_amount_display', 'date')
    search_fields = ('customer_name',)
    readonly_fields = ('total_amount_display',)

    def total_amount_display(self, obj):
        total = sum([item.price * item.quantity for item in obj.items.all()])
        return total
    total_amount_display.short_description = 'Total Amount'

# ---------------- InvoiceItem Admin ----------------
@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = ('invoice', 'product', 'quantity', 'price')
    search_fields = ('product__name', 'invoice__customer_name')
    list_filter = ('product',)
