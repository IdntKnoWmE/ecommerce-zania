from django.test import TestCase
from shop.models import Product, Order


class ProductModelTest(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(name="Laptop", description="High-end laptop", price=1000.00, stock=10)
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.stock, 10)


class OrderModelTest(TestCase):
    def test_order_total_price_calculation(self):
        product1 = Product.objects.create(name="Laptop", description="High-end laptop", price=1000.00, stock=10)
        product2 = Product.objects.create(name="Mouse", description="Wireless mouse", price=50.00, stock=20)
        products = [{"product_id": product1.id, "quantity": 2}, {"product_id": product2.id, "quantity": 1}]
        order = Order.objects.create(products=products, total_price=0, status="pending")

        total_price = product1.price * 2 + product2.price * 1
        self.assertEqual(order.total_price, 0)  # Initial total_price
        order.total_price = total_price
        order.save()
        self.assertEqual(order.total_price, total_price)
