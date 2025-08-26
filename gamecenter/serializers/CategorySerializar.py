import rest_framework.serializers as serializers
from gamecenter.models import Category 

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'