import rest_framework.serializers as serializers
from gamecenter.models import LocalSettings

class LocalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalSettings
        fields = '__all__'