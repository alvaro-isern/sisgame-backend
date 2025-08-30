from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import ProductMaintenance, Product
from ..serializers import ProductMaintenanceSerializer, ProductSerializer

class ProductMaintenanceViewSet(viewsets.ModelViewSet):
    queryset = ProductMaintenance.objects.all()
    serializer_class = ProductMaintenanceSerializer