from rest_framework import viewsets
from gamecenter.models import ProductDevices
from gamecenter.serializers import ProductDevicesSerializer

class ProductDevicesViewSet(viewsets.ModelViewSet):
    queryset = ProductDevices.objects.all()
    serializer_class = ProductDevicesSerializer