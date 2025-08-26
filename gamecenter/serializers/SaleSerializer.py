from rest_framework import serializers
from gamecenter.models import Sale

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')