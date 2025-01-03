import random
from django.core.management.base import BaseCommand

from shop.models import Product


class Command(BaseCommand):
    help = 'Ingest mock data into the Product table'

    def handle(self, *args, **kwargs):
        # List of mock product data
        mock_products = [
            {"name": "Laptop", "description": "A high-performance laptop", "price": 999.99, "stock": 10},
            {"name": "Smartphone", "description": "A feature-packed smartphone", "price": 699.99, "stock": 25},
            {"name": "Headphones", "description": "Noise-canceling headphones", "price": 199.99, "stock": 50},
            {"name": "Keyboard", "description": "Mechanical keyboard with RGB lighting", "price": 89.99, "stock": 40},
            {"name": "Mouse", "description": "Wireless gaming mouse", "price": 59.99, "stock": 30},
        ]

        # Add more random products
        categories = ["Electronics", "Home Appliances", "Sports", "Clothing", "Books"]
        for i in range(1, 11):
            mock_products.append({
                "name": f"Product {i}",
                "description": f"A random {random.choice(categories)} item",
                "price": round(random.uniform(10, 500), 2),
                "stock": random.randint(1, 100),
            })

        # Insert mock data into the Product table
        for product in mock_products:
            Product.objects.get_or_create(
                name=product["name"],
                defaults={
                    "description": product["description"],
                    "price": product["price"],
                    "stock": product["stock"],
                },
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully ingested {len(mock_products)} products into the database!"))
