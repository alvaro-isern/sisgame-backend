from rest_framework import viewsets
from ..models import SaleDetail
from ..serializers import SaleDetailSerializer

class SaleDetailViewSet(viewsets.ModelViewSet):
    queryset = SaleDetail.objects.all()
    serializer_class = SaleDetailSerializer
    