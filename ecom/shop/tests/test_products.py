from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from shop.models import Product, Order


class ProductAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.product_url = "/api/products/"
        self.product_data = {
            "name": "Smartphone",
            "description": "Latest model",
            "price": 500.00,
            "stock": 15
        }

    def test_get_products(self):
        Product.objects.create(**self.product_data)
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Smartphone")

    def test_create_product(self):
        response = self.client.post(self.product_url, self.product_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Smartphone")
        self.assertEqual(response.data["stock"], 15)
