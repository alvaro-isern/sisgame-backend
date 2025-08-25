import rest_framework.serializers as serializers
from gamecenter.models import Subsidiary, LocalSettings
from .LocalSettingsSerializer import LocalSettingsSerializer

class SubsidiarySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    address = serializers.CharField()
    contact_number = serializers.CharField()
    date_opened = serializers.DateField()
    is_main = serializers.BooleanField()
    local_setting = LocalSettingsSerializer()

    class Meta:
        model = Subsidiary
        fields = ['id', 'name', 'address', 'contact_number', 'date_opened', 'is_main', 'local_setting']
        read_only_fields = ['id']

    def create(self, validated_data):
        # Extraer los datos de local_setting
        local_setting_data = validated_data.pop('local_setting')
        
        # Crear o buscar LocalSettings
        local_setting, created = LocalSettings.objects.get_or_create(**local_setting_data)
        
        # Crear Subsidiary con la referencia a LocalSettings
        subsidiary = Subsidiary.objects.create(local_setting=local_setting, **validated_data)
        
        return subsidiary

    def update(self, instance, validated_data):
        # Extraer los datos de local_setting si están presentes
        local_setting_data = validated_data.pop('local_setting', None)
        
        # Actualizar LocalSettings si se proporcionaron datos
        if local_setting_data:
            for attr, value in local_setting_data.items():
                setattr(instance.local_setting, attr, value)
            instance.local_setting.save()
        
        # Actualizar los campos de Subsidiary
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance