from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from shop.models import Product, Order


class OrderAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.order_url = "/api/orders/"
        self.product1 = Product.objects.create(name="Laptop", description="High-end laptop", price=1000.00, stock=10)
        self.product2 = Product.objects.create(name="Mouse", description="Wireless mouse", price=50.00, stock=20)
        self.order_data = {
            "products": [
                {"product_id": self.product1.id, "quantity": 2},
                {"product_id": self.product2.id, "quantity": 1}
            ]
        }

    def test_create_order_successful(self):
        response = self.client.post(self.order_url, self.order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["total_price"], 2050.00)
        self.assertEqual(response.data["status"], "pending")
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock, 8)  # Stock reduced

    def test_create_order_insufficient_stock(self):
        self.order_data["products"][0]["quantity"] = 11  # More than available stock
        response = self.client.post(self.order_url, self.order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Insufficient stock for product ID", response.data["products"][0])

    def test_create_order_product_not_found(self):
        self.order_data["products"].append({"product_id": 999, "quantity": 1})  # Non-existent product
        response = self.client.post(self.order_url, self.order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Product ID 999 does not exist.", response.data["products"][0])
