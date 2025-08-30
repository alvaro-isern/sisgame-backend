import rest_framework.serializers as serializers
from gamecenter.models import ProductGame

class ProductGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGame
        fields = '__all__'