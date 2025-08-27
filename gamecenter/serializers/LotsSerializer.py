from rest_framework import serializers
from gamecenter.models import Lots, Price
from gamecenter.serializers.PriceSerializer import PriceSerializer

class CustomPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ['id', 'unit_measurement', 'sale_price', 'purchase_price']
        
class LotsSerializer(serializers.ModelSerializer):
    price = CustomPriceSerializer()
    product_name = serializers.CharField(source='product.name', read_only=True)
    current_stock = serializers.IntegerField(read_only=True)

    class Meta:
        model = Lots
        fields = ['id', 'lot_number', 'manufacturing_date', 'expiration_date', 
                 'initial_stock', 'current_stock', 'state', 'entry_date', 
                 'observations', 'product', 'product_name', 'price']

    def create(self, validated_data):
        price_data = validated_data.pop('price')
        # Set current_stock to the same value as initial_stock
        initial_stock = validated_data.get('initial_stock', 0)
        validated_data['current_stock'] = initial_stock
        
        lots = Lots.objects.create(**validated_data)
        # Use the same product for price
        price = Price.objects.create(product=lots.product, **price_data)
        lots.price = price
        lots.save()
        return lots

    def update(self, instance, validated_data):
        price_data = validated_data.pop('price', None)
        if price_data:
            if instance.price is None:
                # Create new price if none exists
                price = Price.objects.create(product=instance.product, **price_data)
                instance.price = price
            else:
                # Update existing price
                for attr, value in price_data.items():
                    setattr(instance.price, attr, value)
                instance.price.save()
        
        # If initial_stock is being updated, update current_stock too
        if 'initial_stock' in validated_data:
            validated_data['current_stock'] = validated_data['initial_stock']
        
        # Update lot fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance