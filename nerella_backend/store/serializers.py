from rest_framework import serializers
from .models import Product, Invoice, InvoiceItem
from django.contrib.auth.models import User

# ---------------- User Serializers ----------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user

# ---------------- Product Serializer ----------------
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# ---------------- Invoice Item Serializer ----------------
class InvoiceItemSerializer(serializers.ModelSerializer):
    barcode = serializers.CharField(write_only=True)  # frontend sends barcode

    class Meta:
        model = InvoiceItem
        fields = ['barcode', 'product', 'quantity', 'price']
        extra_kwargs = {'product': {'read_only': True}}

    def create(self, validated_data):
        barcode = validated_data.pop('barcode')
        try:
            product = Product.objects.get(barcode=barcode)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Product with barcode {barcode} not found")

        if product.stock < validated_data['quantity']:
            raise serializers.ValidationError(f"Not enough stock for {product.name}")

        validated_data['product'] = product
        product.stock -= validated_data['quantity']  # deduct stock
        product.save()

        return InvoiceItem.objects.create(**validated_data)


# ---------------- Invoice Serializer ----------------
class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ["id", "customer_name", "total_amount", "date", "items"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        invoice = Invoice.objects.create(**validated_data)

        total_amount = 0
        for item_data in items_data:
            item = InvoiceItemSerializer().create(item_data)
            item.invoice = invoice
            item.save()
            total_amount += item.price * item.quantity

        invoice.total_amount = total_amount
        invoice.save()

        return invoice