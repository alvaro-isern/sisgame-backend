import rest_framework.serializers as serializers
from gamecenter.models import ProductDevices

class ProductDevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDevices
        fields = '__all__'