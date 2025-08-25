from rest_framework import viewsets
from gamecenter.models import Subsidiary
from gamecenter.serializers import SubsidiarySerializer

class SubsidiaryViewSet(viewsets.ModelViewSet):
    queryset = Subsidiary.objects.all()
    serializer_class = SubsidiarySerializer
