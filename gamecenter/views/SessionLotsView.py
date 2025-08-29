from rest_framework import viewsets
from ..models import SessionLots
from ..serializers import SessionLotsSerializer

class SessionLotsViewSet(viewsets.ModelViewSet):
    queryset = SessionLots.objects.all()
    serializer_class = SessionLotsSerializer