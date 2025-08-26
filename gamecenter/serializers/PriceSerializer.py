from rest_framework import serializers
from gamecenter.models import Price

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = '__all__'