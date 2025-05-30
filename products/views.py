from rest_framework import viewsets
from .models import Category, Product, InventoryMovement
from .serializers import ProductSerializer, InventoryMovementSerializer, CategorySerializer
from rest_framework import permissions

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'code'  # Usar código en URL

class InventoryMovementViewSet(viewsets.ModelViewSet):
    queryset = InventoryMovement.objects.all()
    serializer_class = InventoryMovementSerializer

