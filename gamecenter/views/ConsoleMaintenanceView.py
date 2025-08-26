from rest_framework import viewsets
from ..models import ConsoleMaintenance
from ..serializers import ConsoleMaintenanceSerializer

class ConsoleMaintenanceViewSet(viewsets.ModelViewSet):
    queryset = ConsoleMaintenance.objects.all()
    serializer_class = ConsoleMaintenanceSerializer
    
