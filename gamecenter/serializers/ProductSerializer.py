import rest_framework.serializers as serializers
from gamecenter.models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'