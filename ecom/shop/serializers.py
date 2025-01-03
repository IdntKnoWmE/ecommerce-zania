from rest_framework import serializers
from .models import Product, Order


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock']


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.FloatField(read_only=True)  # Mark this field as read-only

    class Meta:
        model = Order
        fields = ['id', 'products', 'total_price', 'status']

    def validate_products(self, products):
        """
        Custom validation to check if there are enough stocks for the order.
        """
        for item in products:
            product_id = item.get("product_id")
            quantity = item.get("quantity")
            try:
                product = Product.objects.get(id=product_id)
                if product.stock < quantity:
                    raise serializers.ValidationError(
                        f"Insufficient stock for product ID {product_id}. Available: {product.stock}, Requested: {quantity}."
                    )
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product ID {product_id} does not exist.")
        return products

    def create(self, validated_data):
        """
        Custom create method to handle stock reduction and order creation.
        """
        products = validated_data.pop('products')
        total_price = 0

        # Deduct stock and calculate total price
        for item in products:
            product_id = item["product_id"]
            quantity = item["quantity"]
            product = Product.objects.get(id=product_id)
            product.stock -= quantity
            product.save()
            total_price += product.price * quantity

        # Create the order
        order = Order.objects.create(total_price=total_price, products=products, **validated_data)
        return order
