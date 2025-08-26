from rest_framework import serializers
from ..models import ConsoleMaintenance

class ConsoleMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsoleMaintenance
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')