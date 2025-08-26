from rest_framework import viewsets
from gamecenter.models import Product
from gamecenter.serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer