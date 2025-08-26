from rest_framework import viewsets
from gamecenter.models import Lots
from gamecenter.serializers import LotsSerializer

class LotViewSet(viewsets.ModelViewSet):
    queryset = Lots.objects.all()
    serializer_class = LotsSerializer