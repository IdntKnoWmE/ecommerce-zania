from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling product-related endpoints.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        """
        Handle POST /products to add a new product.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderViewSet(viewsets.ViewSet):
    """
    ViewSet for handling order-related endpoints.
    """
    def create(self, request, *args, **kwargs):
        """
        Handle POST /orders to place an order.
        """
        serializer = OrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
