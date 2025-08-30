from rest_framework import serializers
from gamecenter.models import SessionLots, Lots

class SessionLotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionLots
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter lots to only include products from "comestibles" category group
        if 'lots' in self.fields:
            self.fields['lots'].queryset = Lots.objects.filter(
                product__category__group__in=['comestibles', 'accesorios'],
            )